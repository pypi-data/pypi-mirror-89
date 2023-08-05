#
# Copyright (C) 2018-2020 University of Oxford
#
# This file is part of tsinfer.
#
# tsinfer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tsinfer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tsinfer.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Manage tsinfer's various file formats.
"""
import collections.abc as abc
import datetime
import itertools
import json
import logging
import os.path
import queue
import sys
import threading
import uuid

import attr
import humanize
import lmdb
import numcodecs
import numpy as np
import tskit
import zarr

import tsinfer.exceptions as exceptions
import tsinfer.provenance as provenance
import tsinfer.threads as threads


logger = logging.getLogger(__name__)


FORMAT_NAME_KEY = "format_name"
FORMAT_VERSION_KEY = "format_version"
FINALISED_KEY = "finalised"

# We use the zstd compressor because it allows for compression of buffers
# bigger than 2GB, which can occur in a larger instances.
DEFAULT_COMPRESSOR = numcodecs.Zstd()

# Lmdb on windows allocates the entire file size rather than
# growing dynamically (see https://github.com/mozilla/lmdb-rs/issues/40).
# For the default setting on windows, we therefore hard code a smaller
# map_size of 1GiB to avoid filling up disk space. On other platforms where
# sparse files are supported, we default to 1TiB.
DEFAULT_MAX_FILE_SIZE = 2 ** 30 if sys.platform == "win32" else 2 ** 40


def permissive_json_schema():
    # A version of this should be in tskit, but we keep it here for now
    # for convenience
    return {
        "codec": "json",
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": True,
    }


def np_obj_equal(np_obj_array1, np_obj_array2):
    """
    A replacement for np.array_equal to test equality of numpy arrays that
    contain objects, as used e.g. for metadata, location, alleles, etc.
    """
    if np_obj_array1.shape != np_obj_array2.shape:
        return False
    return all(itertools.starmap(np.array_equal, zip(np_obj_array1, np_obj_array2)))


def exclude_id(attribute, value):
    """
    Used to filter out the id field from attrs objects such as Ancestor
    """
    return attribute.name != "id"


def remove_lmdb_lockfile(lmdb_file):
    lockfile = lmdb_file + "-lock"
    if os.path.exists(lockfile):
        os.unlink(lockfile)


class BufferedItemWriter:
    """
    Class that writes items sequentially into a set of zarr arrays,
    buffering writes and flushing them to the destination arrays
    asynchronosly using threads.
    """

    def __init__(self, array_map, num_threads=0):
        self.chunk_size = -1
        for array in array_map.values():
            if self.chunk_size == -1:
                self.chunk_size = array.chunks[0]
            else:
                if array.chunks[0] != self.chunk_size:
                    raise ValueError("Chunk sizes must be equal")
        self.arrays = array_map
        if num_threads <= 0:
            # Use a syncronous algorithm.
            self.num_threads = 0
            self.num_buffers = 1
        else:
            # One buffer for each thread. Buffers are referred to by their indexes.
            self.num_buffers = num_threads
            self.num_threads = num_threads
        self.buffers = {}
        self.current_size = 0
        self.total_items = 0
        for key, array in self.arrays.items():
            self.buffers[key] = [None for _ in range(self.num_buffers)]
            np_array = array[:]
            shape = list(array.shape)
            shape[0] = self.chunk_size
            for j in range(self.num_buffers):
                self.buffers[key][j] = np.empty_like(np_array)
                self.buffers[key][j].resize(*shape)
            # Make sure the destination array is zero sized at the start.
            shape[0] = 0
            array.resize(*shape)

        self.start_offset = [0 for _ in range(self.num_buffers)]
        self.num_buffered_items = [0 for _ in range(self.num_buffers)]
        self.write_buffer = 0
        # This lock must be held when resizing the underlying arrays.
        # This is no-op when using a single-threaded algorithm, but it's
        # not worth removing and complicating the logic.
        self.resize_lock = threading.Lock()
        if self.num_threads > 0:
            # Buffer indexes are placed in the queues. The current write buffer
            # is obtained from the write_queue. Flush worker threads pull buffer
            # indexes from the flush queue, and push them back on to the write
            # queue when the buffer has been flushed.
            self.write_queue = queue.Queue()
            self.flush_queue = queue.Queue()
            # The initial write buffer is 0; place the others on the queue.
            for j in range(1, self.num_buffers):
                self.write_queue.put(j)
            # Make the flush threads.
            self.flush_threads = [
                threads.queue_consumer_thread(
                    self._flush_worker,
                    self.flush_queue,
                    name=f"flush-worker-{j}",
                )
                for j in range(self.num_threads)
            ]
            logger.info(f"Started {self.num_threads} flush worker threads")

    def _commit_write_buffer(self, write_buffer):
        start = self.start_offset[write_buffer]
        n = self.num_buffered_items[write_buffer]
        end = start + n
        logger.debug(f"Flushing buffer {write_buffer}: start={start} n={n}")
        with self.resize_lock:
            if self.current_size < end:
                self.current_size = end
                for array in self.arrays.values():
                    shape = list(array.shape)
                    shape[0] = self.current_size
                    array.resize(*shape)
        for key, array in self.arrays.items():
            buffered = self.buffers[key][write_buffer][:n]
            array[start:end] = buffered
        logger.debug(f"Buffer {write_buffer} flush done")

    def _flush_worker(self, thread_index):
        """
        Thread worker responsible for flushing buffers. Read a buffer index
        from flush_queue and write it to disk. Push the index back on
        to the write queue to allow it be reused.
        """
        while True:
            buffer_index = self.flush_queue.get()
            if buffer_index is None:
                break
            self._commit_write_buffer(buffer_index)
            self.flush_queue.task_done()
            self.write_queue.put(buffer_index)
        self.flush_queue.task_done()

    def _queue_flush_buffer(self):
        """
        Flushes the buffered ancestors to the data file.
        """
        if self.num_threads > 0:
            logger.debug(f"Pushing buffer {self.write_buffer} to flush queue")
            self.flush_queue.put(self.write_buffer)
            self.write_buffer = self.write_queue.get()
        else:
            logger.debug("Syncronously flushing buffer")
            self._commit_write_buffer(self.write_buffer)
        self.num_buffered_items[self.write_buffer] = 0
        self.start_offset[self.write_buffer] = self.total_items

    def add(self, **kwargs):
        """
        Add an item to each of the arrays. The keyword arguments for this
        function correspond to the keys in the dictionary of arrays provided
        to the constructor.
        """
        if self.num_buffered_items[self.write_buffer] == self.chunk_size:
            self._queue_flush_buffer()
        offset = self.num_buffered_items[self.write_buffer]
        for key, value in kwargs.items():
            self.buffers[key][self.write_buffer][offset] = value
        self.num_buffered_items[self.write_buffer] += 1
        self.total_items += 1
        return self.total_items - 1

    def flush(self):
        """
        Flush the remaining items to the destination arrays and return all
        items are safely commited.

        It is an error to call ``add`` after ``flush`` has been called.
        """
        self._queue_flush_buffer()
        # Stop the the worker threads.
        for _ in range(self.num_threads):
            self.flush_queue.put(None)
        for j in range(self.num_threads):
            self.flush_threads[j].join()
        self.buffers = None


def zarr_summary(array):
    """
    Returns a string with a brief summary of the specified zarr array.
    """
    dtype = str(array.dtype)
    ret = f"shape={array.shape}; dtype={dtype};"
    if dtype != "object":
        # nbytes doesn't work correctly for object arrays.
        ret += "uncompressed size={}".format(humanize.naturalsize(array.nbytes))
    return ret


def chunk_iterator(array, indexes=None):
    """
    Utility to iterate over closely spaced rows in the specified array efficiently
    by accessing one chunk at a time (normally used as an iterator over each row)
    """
    if indexes is None:
        indexes = range(array.shape[0])
    else:
        if len(indexes) > 0 and (
            np.any(np.diff(indexes) <= 0)
            or indexes[0] < 0
            or indexes[-1] >= array.shape[0]
        ):
            raise ValueError("ids must be positive and in ascending order")

    chunk_size = array.chunks[0]
    prev_chunk_id = -1
    for j in indexes:
        chunk_id = j // chunk_size
        if chunk_id != prev_chunk_id:
            chunk = array[chunk_id * chunk_size : (chunk_id + 1) * chunk_size][:]
            prev_chunk_id = chunk_id
        yield chunk[j % chunk_size]


def merge_variants(sd1, sd2):
    """
    Returns an iterator over the merged variants in the specified
    SampleData files. Sites are merged by site position, and
    genotypes are set to missing data for sites are as not present
    in one of the data files.
    """
    var1_iter = iter(sd1.variants())
    var2_iter = iter(sd2.variants())
    var1 = next(var1_iter, None)
    var2 = next(var2_iter, None)
    n1 = sd1.num_samples
    n2 = sd2.num_samples
    genotypes = np.empty(n1 + n2, dtype=np.int8)
    while var1 is not None and var2 is not None:
        if var1.site.position == var2.site.position:
            # Checking metadata as well is probably overly strict, but
            # we can fix this later if needs be.
            if (
                var1.site.ancestral_state != var2.site.ancestral_state
                or not np.array_equal(var1.site.time, var2.site.time, equal_nan=True)
                or var1.site.metadata != var2.site.metadata
            ):
                raise ValueError(
                    "Merged sites must have the same ancestral_state, "
                    "time and metadata"
                )
            # If there is missing data the last allele is always None
            missing_data = False
            alleles = list(var1.site.alleles)
            if alleles[-1] is None:
                alleles = alleles[:-1]
                missing_data = True
            var2_genotypes = var2.genotypes.copy()
            for old_index, allele in enumerate(var2.site.alleles):
                if allele is None:
                    missing_data = True
                    break
                if allele not in alleles:
                    alleles.append(allele)
                new_index = alleles.index(allele)
                if old_index != new_index:
                    var2_genotypes[var2.genotypes == old_index] = new_index
            if missing_data:
                alleles.append(None)
            genotypes[:n1] = var1.genotypes
            genotypes[n1:] = var2_genotypes
            site = var1.site
            site.alleles = alleles
            # TODO not sure why we have alleles on both the Site and Variant
            var = Variant(site=site, genotypes=genotypes, alleles=alleles)
            yield var
            var1 = next(var1_iter, None)
            var2 = next(var2_iter, None)
        elif var1.site.position < var2.site.position:
            genotypes[:n1] = var1.genotypes
            genotypes[n1:] = tskit.MISSING_DATA
            var1.genotypes = genotypes
            yield var1
            var1 = next(var1_iter, None)
        else:
            genotypes[:n1] = tskit.MISSING_DATA
            genotypes[n1:] = var2.genotypes
            var2.genotypes = genotypes
            yield var2
            var2 = next(var2_iter, None)

    genotypes[n1:] = tskit.MISSING_DATA
    while var1 is not None:
        genotypes[:n1] = var1.genotypes
        var1.genotypes = genotypes
        yield var1
        var1 = next(var1_iter, None)

    genotypes[:n1] = tskit.MISSING_DATA
    while var2 is not None:
        genotypes[n1:] = var2.genotypes
        var2.genotypes = genotypes
        yield var2
        var2 = next(var2_iter, None)


class DataContainer:
    """
    Superclass of objects used to represent a collection of related
    data. Each datacontainer in a wrapper around a zarr group.
    """

    READ_MODE = 0
    BUILD_MODE = 1
    EDIT_MODE = 2

    # Must be defined by subclasses.
    FORMAT_NAME = None
    FORMAT_VERSION = None

    def __init__(
        self,
        *,
        path=None,
        num_flush_threads=0,
        compressor=DEFAULT_COMPRESSOR,
        chunk_size=1024,
        max_file_size=None,
    ):
        self._mode = self.BUILD_MODE
        self._num_flush_threads = num_flush_threads
        self._chunk_size = max(1, chunk_size)
        self._metadata_codec = numcodecs.JSON()
        self._compressor = compressor
        self.data = zarr.group()
        self.path = path
        if path is not None:
            store = self._new_lmdb_store(max_file_size)
            self.data = zarr.open_group(store=store, mode="w")
        self.data.attrs[FORMAT_NAME_KEY] = self.FORMAT_NAME
        self.data.attrs[FORMAT_VERSION_KEY] = self.FORMAT_VERSION
        self.data.attrs["uuid"] = str(uuid.uuid4())

        chunks = self._chunk_size
        provenances_group = self.data.create_group("provenances")
        provenances_group.create_dataset(
            "timestamp",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=object,
            object_codec=self._metadata_codec,
        )
        provenances_group.create_dataset(
            "record",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=object,
            object_codec=self._metadata_codec,
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._mode != self.READ_MODE:
            self.finalise()
        elif self.path is not None:
            self.close()

    def _open_lmbd_readonly(self):
        # We set the mapsize here because LMBD will map 1TB of virtual memory if
        # we don't, making it hard to figure out how much memory we're actually
        # using.
        map_size = None
        try:
            map_size = os.path.getsize(self.path)
        except OSError as e:
            raise exceptions.FileFormatError(str(e)) from e
        try:
            store = zarr.LMDBStore(
                self.path, map_size=map_size, readonly=True, subdir=False, lock=False
            )
        except lmdb.InvalidError as e:
            raise exceptions.FileFormatError(
                "Unknown file format:{}".format(str(e))
            ) from e
        except lmdb.Error as e:
            raise exceptions.FileFormatError(str(e)) from e
        return store

    def _open_readonly(self):
        if self.path is not None:
            store = self._open_lmbd_readonly()
        else:
            # This happens when we finalise an in-memory container.
            store = self.data.store
        self.data = zarr.open(store=store, mode="r")
        self._check_format()
        self._mode = self.READ_MODE

    def _new_lmdb_store(self, map_size=None):
        if os.path.exists(self.path):
            os.unlink(self.path)
        # The existence of a lock-file can confuse things, so delete it.
        remove_lmdb_lockfile(self.path)
        if map_size is None:
            map_size = DEFAULT_MAX_FILE_SIZE
        else:
            map_size = int(map_size)
            if map_size <= 0:
                raise ValueError("max_file_size must be > 0")
        return zarr.LMDBStore(self.path, subdir=False, map_size=map_size)

    @classmethod
    def load(cls, path):
        # Try to read the file. This should raise the correct error if we have a
        # directory, missing file, permissions, etc.
        with open(path):
            pass
        self = cls.__new__(cls)
        self.mode = self.READ_MODE
        self.path = path
        self._open_readonly()
        logger.info(f"Loaded {self.summary()}")
        return self

    def close(self):
        """
        Close this DataContainer. Any read or write operations attempted
        after calling this will fail.
        """
        if self._mode != self.READ_MODE:
            self.finalise()
        if self.data.store is not None:
            self.data.store.close()
        self.data = None
        self.mode = -1

    def copy(self, path=None, max_file_size=None):
        """
        Returns a copy of this DataContainer opened in 'edit' mode. If path
        is specified, this must not be equal to the path of the current
        data container. The new container will have a different UUID to the
        current.
        """
        if self._mode != self.READ_MODE:
            raise ValueError("Cannot copy unless in read mode.")
        if path is not None and self.path is not None:
            if os.path.abspath(path) == os.path.abspath(self.path):
                raise ValueError("Cannot copy to the same file")
        cls = type(self)
        other = cls.__new__(cls)
        other.path = path
        if path is None:
            # Have to work around a fairly weird bug in zarr where if we
            # try to use copy_store on an in-memory array we end up
            # overwriting the original values.
            other.data = zarr.group()
            zarr.copy_all(source=self.data, dest=other.data)
            for key, value in self.data.attrs.items():
                other.data.attrs[key] = value
        else:
            store = other._new_lmdb_store(max_file_size)
            zarr.copy_store(self.data.store, store)
            other.data = zarr.group(store)
        # Set a new UUID
        other.data.attrs["uuid"] = str(uuid.uuid4())
        other.data.attrs[FINALISED_KEY] = False
        other._mode = self.EDIT_MODE
        return other

    def finalise(self):
        """
        Ensures that the state of the data is flushed and writes the
        provenance for the current operation. The specified 'command' is used
        to fill the corresponding entry in the provenance dictionary.
        """
        self._check_write_modes()
        self.data.attrs[FINALISED_KEY] = True
        if self.path is not None:
            store = self.data.store
            store.close()
            logger.debug("Fixing up LMDB file size")
            with lmdb.open(self.path, subdir=False, lock=False, writemap=True) as db:
                # LMDB maps a very large amount of space by default. While this
                # doesn't do any harm, it's annoying because we can't use ls to
                # see the file sizes and the amount of RAM we're mapping can
                # look like it's very large. So, we fix this up so that the
                # map size is equal to the number of pages in use.
                num_pages = db.info()["last_pgno"]
                page_size = db.stat()["psize"]
                db.set_mapsize(num_pages * page_size)
            # Remove the lock file as we don't need it after this point.
            remove_lmdb_lockfile(self.path)
        self._open_readonly()

    def _check_format(self):
        try:
            format_name = self.format_name
            format_version = self.format_version
        except KeyError:
            raise exceptions.FileFormatError("Incorrect file format")
        if format_name != self.FORMAT_NAME:
            raise exceptions.FileFormatError(
                "Incorrect file format: expected '{}' got '{}'".format(
                    self.FORMAT_NAME, format_name
                )
            )
        if format_version[0] < self.FORMAT_VERSION[0]:
            raise exceptions.FileFormatTooOld(
                "Format version {} too old. Current version = {}".format(
                    format_version, self.FORMAT_VERSION
                )
            )
        if format_version[0] > self.FORMAT_VERSION[0]:
            raise exceptions.FileFormatTooNew(
                "Format version {} too new. Current version = {}".format(
                    format_version, self.FORMAT_VERSION
                )
            )

    def _check_build_mode(self):
        if self._mode != self.BUILD_MODE:
            raise ValueError("Invalid operation: must be in build mode")

    def _check_edit_mode(self):
        if self._mode != self.EDIT_MODE:
            raise ValueError("Invalid operation: must be in edit mode")

    def _check_write_modes(self):
        if self._mode not in (self.EDIT_MODE, self.BUILD_MODE):
            raise ValueError("Invalid operation: must be in edit or build mode")

    def _check_finalised(self):
        if not self.finalised:
            error_msg = f"The {self.format_name} file"
            if self.path is not None:
                error_msg = f" at `{self.path}`"
            raise ValueError(error_msg + " is not finalised")

    @property
    def file_size(self):
        """
        Returns the size of the underlying file, or -1 if we do not have a
        file associated.
        """
        ret = -1
        if self.path is not None:
            ret = os.path.getsize(self.path)
        return ret

    def _check_metadata(self, metadata):
        ret = metadata
        if metadata is None:
            ret = {}
        elif not isinstance(metadata, abc.Mapping):
            raise TypeError("Metadata must be a JSON-like dictionary")
        return ret

    def add_provenance(self, timestamp, record):
        """
        Adds a new provenance record with the specified timestamp and record.
        Timestamps should ISO8601 formatted, and record is some JSON encodable
        object.
        """
        if self._mode not in (self.BUILD_MODE, self.EDIT_MODE):
            raise ValueError(
                "Invalid operation: cannot add provenances unless in BUILD "
                "or EDIT mode"
            )
        n = self.num_provenances
        self.provenances_timestamp.resize(n + 1)
        self.provenances_record.resize(n + 1)
        self.provenances_timestamp[n] = timestamp
        self.provenances_record[n] = record

    def record_provenance(self, command=None, **kwargs):
        """
        Records the provenance information for this file using the
        tskit provenances schema.
        """
        timestamp = datetime.datetime.now().isoformat()
        record = provenance.get_provenance_dict(command=command, **kwargs)
        self.add_provenance(timestamp, record)

    def clear_provenances(self):
        """
        Clear all provenances in this instance
        """
        if self._mode not in (self.BUILD_MODE, self.EDIT_MODE):
            raise ValueError(
                "Invalid operation: cannot clear provenances unless in BUILD "
                "or EDIT mode"
            )
        self.provenances_timestamp.resize(0)
        self.provenances_record.resize(0)

    @property
    def format_name(self):
        return self.data.attrs[FORMAT_NAME_KEY]

    @property
    def format_version(self):
        return tuple(self.data.attrs[FORMAT_VERSION_KEY])

    @property
    def finalised(self):
        ret = False
        if FINALISED_KEY in self.data.attrs:
            ret = self.data.attrs[FINALISED_KEY]
        return ret

    @property
    def uuid(self):
        return str(self.data.attrs["uuid"])

    @property
    def num_provenances(self):
        return self.provenances_timestamp.shape[0]

    @property
    def provenances_timestamp(self):
        return self.data["provenances/timestamp"]

    @property
    def provenances_record(self):
        return self.data["provenances/record"]

    def _format_str(self, values):
        """
        Helper function for formatting __str__ output.
        """
        s = ""
        # Quick hack to make sure everything lines up.
        max_key = len("provenances/timestamp")
        for k, v in values:
            s += "{:<{}} = {}\n".format(k, max_key, v)
        return s

    def __eq__(self, other):
        ret = NotImplemented
        if isinstance(other, type(self)):
            ret = self.uuid == other.uuid and self.data_equal(other)
        return ret

    def __str__(self):
        values = [
            ("path", self.path),
            ("file_size", humanize.naturalsize(self.file_size, binary=True)),
            ("format_name", self.format_name),
            ("format_version", self.format_version),
            ("finalised", self.finalised),
            ("uuid", self.uuid),
            ("num_provenances", self.num_provenances),
            ("provenances/timestamp", zarr_summary(self.provenances_timestamp)),
            ("provenances/record", zarr_summary(self.provenances_record)),
        ]
        return self._format_str(values)

    def arrays(self):
        """
        Returns a list of all the zarr arrays in this DataContainer.
        """
        ret = []

        def visitor(name, obj):
            if isinstance(obj, zarr.Array):
                ret.append((name, obj))

        self.data.visititems(visitor)
        return ret

    @property
    def info(self):
        """
        Returns a string containing the zarr info for each array.
        """
        s = str(self.data.info)
        for _, array in self.arrays():
            s += ("-" * 80) + "\n"
            s += str(array.info)
        return s

    def provenances(self):
        """
        Returns an iterator over the (timestamp, record) pairs representing
        the provenances for this data container.
        """
        timestamp = self.provenances_timestamp[:]
        record = self.provenances_record[:]
        for j in range(self.num_provenances):
            yield timestamp[j], record[j]


@attr.s
class Site:
    """
    A single site. Mirrors the definition in tskit with some additional fields.
    """

    # TODO document properly.
    id = attr.ib()
    position = attr.ib()
    ancestral_state = attr.ib()
    metadata = attr.ib()
    time = attr.ib()
    alleles = attr.ib()


@attr.s
class Variant:
    """
    A single variant. Mirrors the definition in tskit.
    """

    # TODO document properly.
    site = attr.ib()
    genotypes = attr.ib()
    alleles = attr.ib()


@attr.s
class Individual:
    """
    An Individual object, representing a single individual which may contain multiple
    *samples* (i.e. phased genomes). For instance, a diploid individual will have
    two sample genomes. This is deliberately similar to a :class:`tskit.Individual`.

    Individuals are created with :meth:`SampleData.add_individual`. If a tree sequence
    is inferred from a sample data file containing individuals, these individuals (and
    the data associated with them) will carry through to the inferred tree sequence.
    """

    # TODO document properly.
    id = attr.ib()
    flags = attr.ib()
    location = attr.ib()
    metadata = attr.ib()
    # the samples attribute is filled in programmatically, not stored per individual
    samples = attr.ib()
    # Not in equivalent tskit object
    population = attr.ib()  # NB: differs from tskit, which stores this per node
    time = attr.ib()  # NB: differs from tskit, which stores this per node


@attr.s
class Sample:
    """
    A Sample object, representing a single haploid genome or chromosome. Several
    Samples can be associated with the same :class:`Individual`: for example a
    diploid individual will have one maternal and one paternal sample.

    If a tree sequence is inferred from a set of samples, each sample will be
    associated with a tskit "node", which will be flagged up with
    :data:`tskit.NODE_IS_SAMPLE`.
    """

    # TODO document properly.
    id = attr.ib()
    individual = attr.ib()


@attr.s
class Population:
    """
    A Population object. Mirrors :class:`tskit.Population`.
    """

    # TODO document properly.
    id = attr.ib()
    metadata = attr.ib()


class SampleData(DataContainer):
    """
    SampleData(sequence_length=0, *, path=None, num_flush_threads=0, \
    compressor=DEFAULT_COMPRESSOR, chunk_size=1024, max_file_size=None)

    Class representing input sample data used for inference.
    See sample data file format :ref:`specifications <sec_file_formats_samples>`
    for details on the structure of this file.

    The most common usage for this class will be to import data from some
    external source and save it to file for later use. This will usually
    follow a pattern like:

    .. code-block:: python

        sample_data = tsinfer.SampleData(path="mydata.samples")
        sample_data.add_site(position=1234, genotypes=[0, 0, 1, 0], alleles=["G", "C"])
        sample_data.add_site(position=5678, genotypes=[1, 1, 1, 0], alleles=["A", "T"])
        sample_data.finalise()

    This creates a sample data file for four haploid samples and two sites, and
    saves it in the file "mydata.samples". Note that the call to
    :meth:`.finalise` is essential here to ensure that all data will be
    correctly flushed to disk. For convenience, a context manager may
    also be used to ensure this is done:

    .. code-block:: python

        with tsinfer.SampleData(path="mydata.samples") as sample_data:
            sample_data.add_site(1234, [0, 0, 1, 0], ["G", "C"])
            sample_data.add_site(5678, [1, 1, 1, 0], ["A", "T"])

    More complex :ref:`data models <sec_inference_data_model>` consisting
    of populations and polyploid individuals can also be specified. For
    example, we might have:

    .. code-block:: python

        with tsinfer.SampleData(path="mydata.samples") as sample_data:
            # Define populations
            sample_data.add_population(metadata={"name": "CEU"})
            sample_data.add_population(metadata={"name": "YRI"})
            # Define individuals
            sample_data.add_individual(ploidy=2, population=0, metadata={"name": "NA12"})
            sample_data.add_individual(ploidy=2, population=0, metadata={"name": "NA13"})
            sample_data.add_individual(ploidy=2, population=0, metadata={"name": "NA14"})
            sample_data.add_individual(ploidy=2, population=1, metadata={"name": "NA15"})
            # Define sites and genotypes
            sample_data.add_site(1234, [0, 1, 1, 1, 0, 0, 0, 0], ["G", "C"])
            sample_data.add_site(5678, [0, 0, 0, 0, 0, 0, 1, 1], ["A", "T"])

    In this example we defined two populations and four diploid individuals,
    and so our genotypes arrays are of length eight. Thus, at first site the
    first individual is heterozygous, the second is homozygous with the derived
    allele and the other two individuals are homozygous with the ancestral
    allele. To illustrate how we can use site and population metadata to link
    up with external data sources we use the 1000 genomes identifiers (although
    of course the genotype data is fake). Here we suppose that we have the
    famous NA12878 trio from the CEU population, and one other individual from
    the YRI population. This metadata is then embedded in the final tree
    sequence that we infer, allowing us to use it conveniently in downstream
    analyses.

    .. note:: If a ``path`` is specified, the ``max_file_size`` option puts an
        upper limit on the possible size of the created file. On non-Windows
        systems, space for this file is not immediately allocated but just
        "reserved" using sparse file systems. However, on Windows systems
        the file is allocated immediately, so ``max_file_size`` takes a smaller
        default value, to avoid allocating very large files for no reason.
        Users who wish to run large inferences on Windows may therefore need to
        explictly set an appropriate ``max_file_size``. Note that the
        ``max_file_size`` is only used while the file is being built: one the
        file has been finalised, it is shrunk to its minimum size.

    :param float sequence_length: If specified, this is the sequence length
        that will be associated with the tree sequence output by
        :func:`tsinfer.infer` and :func:`tsinfer.match_samples`. If provided
        site coordinates must be less than this value.
    :param str path: The path of the file to store the sample data. If None,
        the information is stored in memory and not persistent.
    :param int num_flush_threads: The number of background threads to use
        for compressing data and flushing to disc. If <= 0, do not spawn
        any threads but use a synchronous algorithm instead. Default=0.
    :param numcodecs.abc.Codec compressor: A :class:`numcodecs.abc.Codec`
        instance to use for compressing data. Any codec may be used, but
        problems may occur with very large datasets on certain codecs as
        they cannot compress buffers >2GB. If None, do not use any compression.
        Default=:class:`numcodecs.zstd.Zstd`.
    :param int chunk_size: The chunk size used for
        `zarr arrays <http://zarr.readthedocs.io/>`_. This affects
        compression level and algorithm performance. Default=1024.
    :param int max_file_size: If a file is being used to store this data, set
        a maximum size in bytes for the stored file. If None, the default
        value of 1GiB (2**30 bytes) is used on Windows and 1TiB (2**40 bytes)
        on other platforms (see above for details).
    """

    FORMAT_NAME = "tsinfer-sample-data"
    FORMAT_VERSION = (5, 0)

    # State machine for handling automatic addition of samples.
    ADDING_POPULATIONS = 0
    ADDING_SAMPLES = 1
    ADDING_SITES = 2

    def __init__(self, sequence_length=0, **kwargs):

        super().__init__(**kwargs)
        self.data.attrs["sequence_length"] = float(sequence_length)
        self.data.attrs["metadata"] = {}
        self.data.attrs["metadata_schema"] = permissive_json_schema()
        chunks = (self._chunk_size,)
        populations_group = self.data.create_group("populations")
        metadata = populations_group.create_dataset(
            "metadata",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=object,
            object_codec=self._metadata_codec,
        )
        populations_group.attrs["metadata_schema"] = None
        self._populations_writer = BufferedItemWriter(
            {"metadata": metadata}, num_threads=self._num_flush_threads
        )

        individuals_group = self.data.create_group("individuals")
        individuals_group.attrs["metadata_schema"] = None
        metadata = individuals_group.create_dataset(
            "metadata",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=object,
            object_codec=self._metadata_codec,
        )
        location = individuals_group.create_dataset(
            "location",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype="array:f8",
        )
        time = individuals_group.create_dataset(
            "time",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.float64,
        )
        population = individuals_group.create_dataset(
            "population",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.int32,
        )
        flags = individuals_group.create_dataset(
            "flags",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.uint32,
        )
        self._individuals_writer = BufferedItemWriter(
            {
                "metadata": metadata,
                "location": location,
                "time": time,
                "population": population,
                "flags": flags,
            },
            num_threads=self._num_flush_threads,
        )

        samples_group = self.data.create_group("samples")
        individual = samples_group.create_dataset(
            "individual",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.int32,
        )
        self._samples_writer = BufferedItemWriter(
            {"individual": individual},
            num_threads=self._num_flush_threads,
        )

        sites_group = self.data.create_group("sites")
        sites_group.attrs["metadata_schema"] = None
        sites_group.create_dataset(
            "position",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.float64,
        )
        sites_group.create_dataset(
            "time",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.float64,
        )
        sites_group.create_dataset(
            "genotypes",
            shape=(0, 0),
            chunks=(self._chunk_size, self._chunk_size),
            compressor=self._compressor,
            dtype=np.int8,
        )
        sites_group.create_dataset(
            "alleles",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=object,
            object_codec=self._metadata_codec,
        )
        sites_group.create_dataset(
            "metadata",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=object,
            object_codec=self._metadata_codec,
        )

        self._last_position = 0
        self._sites_writer = None
        # We are initially in the ADDING_POPULATIONS state.
        self._build_state = self.ADDING_POPULATIONS

    def summary(self):
        return "SampleData(num_samples={}, num_sites={})".format(
            self.num_samples, self.num_sites
        )

    # Note: abstracting the process of getting and setting the metadata schemas
    # out here so we can do better validation of the inputs/optionally accept
    # a tskit MetadataSchema object rather than a dict.
    def __metadata_schema_getter(self, zarr_group):
        return zarr_group.attrs["metadata_schema"]

    def __metadata_schema_setter(self, zarr_group, schema):
        # Make sure we can parse it.
        if schema is not None:
            parsed_schema = tskit.MetadataSchema(schema)
            # We only support the JSON codec for now for simplicity.
            if parsed_schema.schema["codec"] != "json":
                raise ValueError("Only the JSON codec is currently supported")
        zarr_group.attrs["metadata_schema"] = schema

    @property
    def sequence_length(self):
        return self.data.attrs["sequence_length"]

    @property
    def metadata_schema(self):
        return self.data.attrs["metadata_schema"]

    @metadata_schema.setter
    def metadata_schema(self, schema):
        if schema is None:
            raise ValueError("Must have a schema for top-level metadata")
        self.__metadata_schema_setter(self.data, schema)

    @property
    def metadata(self):
        return self.data.attrs["metadata"]

    @metadata.setter
    def metadata(self, metadata):
        self.data.attrs["metadata"] = metadata

    @property
    def populations_metadata_schema(self):
        return self.__metadata_schema_getter(self.data["populations"])

    @populations_metadata_schema.setter
    def populations_metadata_schema(self, schema):
        self.__metadata_schema_setter(self.data["populations"], schema)

    @property
    def individuals_metadata_schema(self):
        return self.__metadata_schema_getter(self.data["individuals"])

    @individuals_metadata_schema.setter
    def individuals_metadata_schema(self, schema):
        self.__metadata_schema_setter(self.data["individuals"], schema)

    @property
    def sites_metadata_schema(self):
        return self.__metadata_schema_getter(self.data["sites"])

    @sites_metadata_schema.setter
    def sites_metadata_schema(self, schema):
        self.__metadata_schema_setter(self.data["sites"], schema)

    @property
    def num_populations(self):
        return self.populations_metadata.shape[0]

    @property
    def num_samples(self):
        return self.samples_individual.shape[0]

    @property
    def num_individuals(self):
        return self.individuals_metadata.shape[0]

    @property
    def num_sites(self):
        return self.sites_position.shape[0]

    @property
    def populations_metadata(self):
        return self.data["populations/metadata"]

    @property
    def individuals_metadata(self):
        return self.data["individuals/metadata"]

    @property
    def individuals_location(self):
        return self.data["individuals/location"]

    @property
    def individuals_time(self):
        return self.data["individuals/time"]

    @property
    def individuals_population(self):
        return self.data["individuals/population"]

    @property
    def individuals_flags(self):
        return self.data["individuals/flags"]

    @property
    def samples_individual(self):
        return self.data["samples/individual"]

    @property
    def sites_genotypes(self):
        return self.data["sites/genotypes"]

    @property
    def sites_position(self):
        return self.data["sites/position"]

    @property
    def sites_time(self):
        return self.data["sites/time"]

    @sites_time.setter
    def sites_time(self, value):
        self._check_edit_mode()
        self.data["sites/time"][:] = np.array(value, dtype=np.float64, copy=False)

    @property
    def sites_alleles(self):
        return self.data["sites/alleles"]

    @property
    def sites_metadata(self):
        return self.data["sites/metadata"]

    def __str__(self):
        values = [
            ("sequence_length", self.sequence_length),
            ("metadata_schema", self.metadata_schema),
            ("metadata", self.metadata),
            ("num_populations", self.num_populations),
            ("num_individuals", self.num_individuals),
            ("num_samples", self.num_samples),
            ("num_sites", self.num_sites),
            ("populations/metadata_schema", self.populations_metadata_schema),
            ("populations/metadata", zarr_summary(self.populations_metadata)),
            ("individuals/metadata_schema", self.individuals_metadata_schema),
            ("individuals/metadata", zarr_summary(self.individuals_metadata)),
            ("individuals/location", zarr_summary(self.individuals_location)),
            ("individuals/time", zarr_summary(self.individuals_time)),
            ("individuals/population", zarr_summary(self.individuals_population)),
            ("individuals/flags", zarr_summary(self.individuals_flags)),
            ("samples/individual", zarr_summary(self.samples_individual)),
            ("sites/position", zarr_summary(self.sites_position)),
            ("sites/time", zarr_summary(self.sites_time)),
            ("sites/alleles", zarr_summary(self.sites_alleles)),
            ("sites/genotypes", zarr_summary(self.sites_genotypes)),
            ("sites/metadata_schema", self.sites_metadata_schema),
            ("sites/metadata", zarr_summary(self.sites_metadata)),
        ]
        return super().__str__() + self._format_str(values)

    def formats_equal(self, other):
        return (
            self.format_name == other.format_name
            and self.format_version == other.format_version
        )

    def populations_equal(self, other):
        return (
            self.num_populations == other.num_populations
            # Need to take a different approach with np object arrays.
            and np_obj_equal(
                self.populations_metadata[:], other.populations_metadata[:]
            )
        )

    def individuals_equal(self, other):
        return (
            self.num_individuals == other.num_individuals
            and np.allclose(
                self.individuals_time[:], other.individuals_time[:], equal_nan=True
            )
            and np.array_equal(self.individuals_flags[:], other.individuals_flags[:])
            and np.array_equal(
                self.individuals_population[:], other.individuals_population[:]
            )
            and np_obj_equal(
                self.individuals_metadata[:], other.individuals_metadata[:]
            )
            and np_obj_equal(
                self.individuals_location[:], other.individuals_location[:]
            )
        )

    def samples_equal(self, other):
        return self.num_samples == other.num_samples and np.all(
            self.samples_individual[:] == other.samples_individual[:]
        )

    def sites_equal(self, other):
        return (
            self.num_sites == other.num_sites
            and np.all(self.sites_position[:] == other.sites_position[:])
            and np.all(self.sites_genotypes[:] == other.sites_genotypes[:])
            and np.allclose(self.sites_time[:], other.sites_time[:], equal_nan=True)
            and np_obj_equal(self.sites_metadata[:], other.sites_metadata[:])
            and np_obj_equal(self.sites_alleles[:], other.sites_alleles[:])
        )

    def data_equal(self, other):
        """
        Returns True if all the data attributes of this input file and the
        specified input file are equal. This compares every attribute except
        the UUID and provenance.

        To compare two :class:`SampleData` instances for exact equality of
        all data including UUIDs and provenance data, use ``s1 == s2``.

        :param SampleData other: The other :class:`SampleData` instance to
            compare with.
        :return: ``True`` if the data held in this :class:`SampleData`
            instance is identical to the date held in the other instance.
        :rtype: bool
        """
        return (
            self.sequence_length == other.sequence_length
            and self.formats_equal(other)
            and self.populations_equal(other)
            and self.individuals_equal(other)
            and self.samples_equal(other)
            and self.sites_equal(other)
        )

    def assert_data_equal(self, other):
        """
        The same as :meth:`.data_equal`, but raises an assertion rather than returning
        False. This is useful for testing.
        """
        assert self.sequence_length == other.sequence_length
        assert self.formats_equal(other)
        assert self.populations_equal(other)
        assert self.individuals_equal(other)
        assert self.samples_equal(other)
        assert self.sites_equal(other)

    def subset(self, individuals=None, sites=None, **kwargs):
        """
        Returns a subset of this sample data file consisting of the specified
        individuals and sites. It is important to note that these are
        *individual* IDs and not *sample* IDs (corresponding to distinct
        haplotypes within an individual). When working with haploid data, the
        individual and site IDs are guaranteed to be the same, and so can be
        used interchangably.

        :param arraylike individuals: The individual IDs to retain in the
            returned subset. IDs must be unique, and refer to valid individuals
            in the current dataset. IDs can be supplied in any order,
            and the order will be preserved in the returned data file (i.e.,
            ``individuals[0]`` will be the first individual in the new
            dataset, etc).
        :param arraylike sites: The site IDs to retain in the
            returned subset. IDs must be unique, and refer to valid sites
            in the current dataset. Site IDs can be supplied in any order,
            but the order will *not* be preserved in the returned data file,
            so that sites are always in position sorted order in the output.
        :param \\**kwargs: Further arguments passed to the :class:`SampleData`
            constructor.
        :return: A :class:`.SampleData` object.
        :rtype: SampleData
        """
        if individuals is None:
            individuals = np.arange(self.num_individuals)
        individuals = np.array(individuals, dtype=np.int32)
        if np.any(individuals < 0) or np.any(individuals >= self.num_individuals):
            raise ValueError("Individual ID out of bounds")
        if len(set(individuals)) != len(individuals):
            raise ValueError("Duplicate individual IDs")
        if sites is None:
            sites = np.arange(self.num_sites)
        sites = np.array(sites, dtype=np.int32)
        if np.any(sites < 0) or np.any(sites >= self.num_sites):
            raise ValueError("Site ID out of bounds")
        num_sites = len(sites)
        # Store the sites as a set for quick lookup.
        sites = set(sites)
        if len(sites) != num_sites:
            raise ValueError("Duplicate site IDS")
        with SampleData(sequence_length=self.sequence_length, **kwargs) as subset:
            # NOTE We don't bother filtering the populations, but we could.
            for population in self.populations():
                subset.add_population(population.metadata)
            sample_selection = []
            for individual_id in individuals:
                individual = self.individual(individual_id)
                sample_selection.extend(individual.samples)
                subset.add_individual(
                    location=individual.location,
                    metadata=individual.metadata,
                    time=individual.time,
                    population=individual.population,
                    ploidy=len(individual.samples),
                )
            sample_selection = np.array(sample_selection, dtype=int)
            if len(sample_selection) < 2:
                raise ValueError("Must have at least two samples")
            for variant in self.variants():
                if variant.site.id in sites:
                    subset.add_site(
                        position=variant.site.position,
                        genotypes=variant.genotypes[sample_selection],
                        alleles=variant.alleles,
                        metadata=variant.site.metadata,
                        time=variant.site.time,
                    )
            for timestamp, record in self.provenances():
                subset.add_provenance(timestamp, record)
            subset.record_provenance(command="subset", **kwargs)
        return subset

    def min_site_times(self, individuals_only=False):
        """
        Returns a numpy array of the lower bound of the time of sites in the SampleData
        file. Each individual with a nonzero time (from the individuals_time array)
        gives a lower bound on the age of sites where the individual carries a
        derived allele.

        :return: A numpy array of the lower bound for each sites time.
        :rtype: numpy.ndarray(dtype=float64)
        """
        samples_individual = self.samples_individual[:]
        assert np.all(samples_individual >= 0)
        samples_time = self.individuals_time[:][samples_individual]
        if np.any(samples_time < 0):
            raise ValueError("Individuals cannot have negative times")
        historical_samples = samples_time != 0
        historical_samples_time = samples_time[historical_samples]
        sites_bound = np.zeros(self.num_sites)
        for var in self.variants():
            historical_genos = var.genotypes[historical_samples]
            derived = historical_genos > 0
            if np.any(derived):
                historical_bound = np.max(historical_samples_time[derived])
                if historical_bound > sites_bound[var.site.id]:
                    sites_bound[var.site.id] = historical_bound
        if not individuals_only:
            sites_bound = np.maximum(self.sites_time[:], sites_bound)
        return sites_bound

    ####################################
    # Write mode
    ####################################

    @classmethod
    def from_tree_sequence(
        cls,
        ts,
        use_sites_time=True,
        use_individuals_time=True,
        **kwargs,
    ):
        """
        Create a SampleData instance from the sample nodes in an existing tree sequence.
        Each sample node in the tree sequence results in a sample created in the returned
        object. Populations in the tree sequence will be copied into the returned object.
        Individuals in the tree sequence that are associated with any sample nodes will
        also be incorporated: the ploidy of each individual is assumed to be the number
        of sample nodes which reference that individual; individuals with no sample nodes
        are omitted. A new haploid individual is created for any sample node which lacks
        an associated individual in the existing tree sequence. Thus a tree sequence
        with ``u`` sample nodes but no individuals will be translated into a SampleData
        file with ``u`` haploid individuals and ``u`` samples.

        Metadata associated with individuals, populations, sites, and at the top level
        of the tree sequence, is also stored in the appropriate places in the returned
        SampleData instance. Any such metadata must either have a schema defined
        or be JSON encodable text. See the `tskit documentation
        <https://tskit.readthedocs.io/en/stable/metadata.html>`_ for more details
        on metadata schemas.

        :param TreeSequence ts: The :class:`tskit.TreeSequence` from which to generate
            samples.
        :param bool use_sites_time: If True (default), the times of nodes in the tree
            sequence are used to set a time for each site (which affects the relative
            temporal order of ancestors during inference). Times for a site are only
            used if there is a single mutation at that site, in which case the node
            immediately below the mutation is taken as the origination time for the
            variant. If False, the frequency of the variant is used as a proxy for the
            relative variant time (see :meth:`.add_site`).
        :param bool use_individuals_time: If True (default), set a time for individuals
            that contain historical sample nodes. If False, all individuals are
            set at time 0.
        :param \\**kwargs: Further arguments passed to the :class:`SampleData`
            constructor.
        :return: A :class:`.SampleData` object.
        :rtype: SampleData
        """

        def encode_metadata(metadata, schema):
            if schema is None:
                if len(metadata) > 0:
                    metadata = json.loads(metadata)
                else:
                    metadata = None
            return metadata

        tables = ts.tables
        self = cls(sequence_length=ts.sequence_length, **kwargs)

        schema = tables.metadata_schema.schema
        if schema is not None:
            self.metadata_schema = schema
            self.metadata = tables.metadata
        else:
            assert len(tables.metadata) == 0

        schema = tables.populations.metadata_schema.schema
        self.populations_metadata_schema = schema
        for population in ts.populations():
            self.add_population(metadata=encode_metadata(population.metadata, schema))

        schema = tables.individuals.metadata_schema.schema
        self.individuals_metadata_schema = schema
        for individual in ts.individuals():
            nodes = individual.nodes
            if len(nodes) > 0:
                first_node = ts.node(nodes[0])
                for u in nodes[1:]:
                    if ts.node(u).time != first_node.time:
                        raise ValueError(
                            "All nodes for individual {} must have the same time".format(
                                individual.id
                            )
                        )
                    if ts.node(u).population != first_node.population:
                        raise ValueError(
                            "All nodes for individual {} must be in the same "
                            "population".format(individual.id)
                        )
                metadata = encode_metadata(individual.metadata, schema)
                self.add_individual(
                    location=individual.location,
                    metadata=metadata,
                    population=first_node.population,
                    flags=individual.flags,
                    time=first_node.time if use_individuals_time else 0,
                    ploidy=len(nodes),
                )
        for u in ts.samples():
            node = ts.node(u)
            if node.individual == tskit.NULL:
                # The sample node has no individual: create a haploid individual for it
                self.add_individual(
                    population=node.population,
                    time=node.time if use_individuals_time else 0,
                    ploidy=1,
                )

        schema = tables.sites.metadata_schema.schema
        self.sites_metadata_schema = schema
        for v in ts.variants():
            variant_time = tskit.UNKNOWN_TIME
            if use_sites_time:
                variant_time = np.nan
                if len(v.site.mutations) == 1:
                    variant_time = ts.node(v.site.mutations[0].node).time
            self.add_site(
                v.site.position,
                v.genotypes,
                v.alleles,
                metadata=encode_metadata(v.site.metadata, schema),
                time=variant_time,
            )
        # Insert all the provenance from the original tree sequence.
        for prov in ts.provenances():
            self.add_provenance(prov.timestamp, json.loads(prov.record))
        self.record_provenance(command="from-tree-sequence", **kwargs)
        self.finalise()
        return self

    def _alloc_site_writer(self):
        if self.num_samples < 2:
            raise ValueError("Must have at least 2 samples")
        self.sites_genotypes.resize(0, self.num_samples)
        arrays = {
            "position": self.sites_position,
            "genotypes": self.sites_genotypes,
            "alleles": self.sites_alleles,
            "metadata": self.sites_metadata,
            "time": self.sites_time,
        }
        self._sites_writer = BufferedItemWriter(
            arrays, num_threads=self._num_flush_threads
        )

    def add_population(self, metadata=None):
        """
        Adds a new :ref:`sec_inference_data_model_population` to this
        :class:`.SampleData` and returns its ID.

        All calls to this method must be made **before** individuals or sites
        are defined.

        :param dict metadata: A JSON encodable dict-like object containing
            metadata that is to be associated with this population.
        :return: The ID of the newly added population.
        :rtype: int
        """
        self._check_build_mode()
        if self._build_state != self.ADDING_POPULATIONS:
            raise ValueError("Cannot add populations after adding samples or sites")
        return self._populations_writer.add(metadata=self._check_metadata(metadata))

    def add_individual(
        self,
        ploidy=1,
        metadata=None,
        population=None,
        location=None,
        time=0,
        flags=None,
    ):
        """
        Adds a new :ref:`sec_inference_data_model_individual` to this
        :class:`.SampleData` and returns its ID and those of the resulting additional
        samples. Adding an individual with ploidy ``k`` results in ``k`` new samples
        being added, and each of these samples will be associated with the
        new individual. Each new sample will also be associated with the specified
        population ID. It is an error to specify a population ID that does not
        correspond to a population defined using :meth:`.add_population`.

        All calls to this method must be made **after** populations are defined
        using :meth:`.add_population` and **before** sites are defined using
        :meth:`.add_site`.

        :param int ploidy: The ploidy of this individual. This corresponds to the
            number of samples added that refer to this individual. Defaults to 1
            (haploid).
        :param dict metadata: A JSON encodable dict-like object containing
            metadata that is to be associated with this individual.
        :param int population: The ID of the population to associate with this
            individual (or more precisely, with the samples for this individual).
            If not specified or None, defaults to the null population (-1).
        :param arraylike location: An array-like object defining n-dimensional
            spatial location of this individual. If not specified or None, the
            empty location is stored.
        :param float time: The historical time into the past when the samples
            associated with this individual were taken. By default we assume that
            all samples come from the present time (i.e. the default time is 0).
        :param int flags: The bitwise flags for this individual.
        :return: The ID of the newly added individual and a list of the sample
            IDs also added.
        :rtype: tuple(int, list(int))
        """
        self._check_build_mode()
        if self._build_state == self.ADDING_POPULATIONS:
            self._populations_writer.flush()
            self._populations_writer = None
            self._build_state = self.ADDING_SAMPLES
        if self._build_state != self.ADDING_SAMPLES:
            raise ValueError("Cannot add individuals after adding sites")

        time = np.float64(time).item()
        if not np.isfinite(time):
            raise ValueError("time must be a single finite number")
        if population is None:
            population = tskit.NULL
        if population >= self.num_populations:
            raise ValueError("population ID out of bounds")
        if ploidy <= 0:
            raise ValueError("Ploidy must be at least 1")
        if location is None:
            location = []
        location = np.array(location, dtype=np.float64)
        if flags is None:
            flags = 0
        individual_id = self._individuals_writer.add(
            metadata=self._check_metadata(metadata),
            location=location,
            time=time,
            population=population,
            flags=flags,
        )
        sample_ids = []
        for _ in range(ploidy):
            sid = self._samples_writer.add(
                individual=individual_id,
            )
            sample_ids.append(sid)
        return individual_id, sample_ids

    def add_site(
        self,
        position,
        genotypes,
        alleles=None,
        metadata=None,
        inference=None,
        time=None,
    ):
        """
        Adds a new site to this :class:`.SampleData` and returns its ID.

        At a minimum, the new site must specify the ``position`` and
        ``genotypes``. Sites must be added in increasing order of position;
        duplicate positions are **not** supported. For each site a list of
        ``alleles`` may be supplied. This list defines the ancestral and
        derived states at the site. For example, if we set ``alleles=["A",
        "T"]`` then the ancestral state is "A" and the derived state is "T".
        The observed state for each sample is then encoded using the
        ``genotypes`` parameter. Thus if we have ``n`` samples then
        this must be a one dimensional array-like object with length ``n``.
        The ``genotypes`` index into the list of ``alleles``, so that for
        a given array ``g`` and sample index ``j``, ``g[j]`` should contain
        ``0`` if sample ``j`` carries the ancestral state at this site and
        ``1`` if it carries the derived state. For multiple derived states,
        there may be more than 2 ``alleles`, and ``g[j]`` can be greater
        than ``1``, but such sites are not used for inference. All sites must
        have genotypes for the same number of samples.

        All populations and individuals must be defined **before** this method
        is called. If no individuals have been defined using
        :meth:`.add_individual`, the first call to this method adds ``n``
        haploid individuals, where ``n`` is the length of the ``genotypes``
        array.

        :param float position: The floating point position of this site. Must be
            less than the ``sequence_length`` if provided to the :class:`.SampleData`
            constructor. Must be greater than all previously added sites.
        :param arraylike genotypes: An array-like object defining the sample
            genotypes at this site. The array of genotypes corresponds to the
            observed alleles for each sample, represented by indexes into the
            alleles array. Missing sample data can be represented by tskit.MISSING_DATA
            in this array. The input is converted to a numpy array with
            dtype ``np.int8``; therefore, for maximum efficiency ensure
            that the input array is also of this type.
        :param list(str) alleles: A list of strings defining the alleles at this
            site. The zero'th element of this list is the **ancestral state**
            and further elements are the **derived states**. Only biallelic
            sites can currently be used for inference. Sites with 3 or more
            alleles cannot have ``inference`` (below) set to ``True``. If not
            specified or None, defaults to ["0", "1"].
        :param dict metadata: A JSON encodable dict-like object containing
            metadata that is to be associated with this site.
        :param float time: The time of occurence (pastwards) of the mutation to the
            derived state at this site. If not specified or None, the frequency of the
            derived alleles (i.e., the proportion of non-zero values in the genotypes,
            out of all the non-missing values) will be used in inference. For
            biallelic sites this frequency should provide a reasonable estimate
            of the relative time, as used to order ancestral haplotypes during the
            inference process. For sites not used in inference, such as singletons or
            sites with more than two alleles or when the time is specified as
            ``np.nan``, then the value is unused. Defaults to None.
        :return: The ID of the newly added site.
        :rtype: int
        """
        genotypes = tskit.util.safe_np_int_cast(genotypes, dtype=np.int8)
        self._check_build_mode()
        if self._build_state == self.ADDING_POPULATIONS:
            if genotypes.shape[0] == 0:
                # We could just raise an error here but we set the state
                # here so that we can raise the same error as other
                # similar conditions.
                self._build_state = self.ADDING_SAMPLES
            else:
                # Add in the default haploid samples.
                for _ in range(genotypes.shape[0]):
                    self.add_individual()
        if self._build_state == self.ADDING_SAMPLES:
            self._individuals_writer.flush()
            self._samples_writer.flush()
            self._alloc_site_writer()
            self._build_state = self.ADDING_SITES
            self._last_position = -1
        assert self._build_state == self.ADDING_SITES

        if alleles is None:
            alleles = ["0", "1"]
        n_alleles = len(alleles)
        non_missing = genotypes != tskit.MISSING_DATA
        if len(set(alleles)) != n_alleles:
            raise ValueError("Alleles must be distinct")
        if n_alleles > 64:
            # This is mandated by tskit's map_mutations function.
            raise ValueError("Cannot have more than 64 alleles")
        if np.any(genotypes == tskit.MISSING_DATA) and alleles[-1] is not None:
            # Don't modify the input parameter
            alleles = list(alleles) + [None]
        if np.any(np.logical_and(genotypes < 0, genotypes != tskit.MISSING_DATA)):
            raise ValueError("Non-missing values for genotypes cannot be negative")
        if genotypes.shape != (self.num_samples,):
            raise ValueError(f"Must have {self.num_samples} (num_samples) genotypes.")
        if np.any(genotypes[non_missing] >= n_alleles):
            raise ValueError("Non-missing values for genotypes must be < num alleles")
        if position < 0:
            raise ValueError("Site position must be > 0")
        if self.sequence_length > 0 and position >= self.sequence_length:
            raise ValueError("Site position must be less than the sequence length")
        if position <= self._last_position:
            raise ValueError(
                "Site positions must be unique and added in increasing order"
            )
        if inference is not None:
            raise ValueError(
                "Inference sites no longer be stored in the sample data file. "
                "Please use the exclude_sites option to generate_ancestors."
            )
        if time is None:
            time = tskit.UNKNOWN_TIME
        site_id = self._sites_writer.add(
            position=position,
            genotypes=genotypes,
            metadata=self._check_metadata(metadata),
            alleles=alleles,
            time=time,
        )
        self._last_position = position
        return site_id

    def append_sites(self, *additional_samples):
        # Append sites from additional sample data objects to the current object. This
        # allows input files (e.g. vcf files) to be read in parallel into separate
        # sample data files and the combined together. The additional samples should have
        # exactly the same populations, individuals, and samples, but with additional
        # sites. The additional sample data objects must be provided in the correct order
        # such that site positions are monotonically ascending.
        # The method is deliberately undocumented, as a more capable way of representing
        # variant data is planned in the future, which should include this functionality.
        self._check_write_modes()
        last_pos = self.sites_position[-1]
        for other in additional_samples:
            other._check_finalised()
            if other.sites_position[0] <= last_pos:
                raise ValueError(
                    "sample data files must be in ascending order of genome position"
                )
            last_pos = other.sites_position[-1]
            if not self.sequence_length == other.sequence_length:
                raise ValueError("sample data files must have the same sequence length")
            if not self.formats_equal(other):
                raise ValueError("sample data files must be of the same format")
            if not self.samples_equal(other):
                raise ValueError("sample data files must have identical samples")
            if not self.individuals_equal(other):
                raise ValueError("sample data files must have identical individuals")
            if not self.populations_equal(other):
                raise ValueError("sample data files must have identical populations")
        for other in additional_samples:
            for name, arr in self.arrays():
                if name.startswith("sites/"):
                    arr.append(other.data[name])

    def finalise(self):
        if self._mode == self.BUILD_MODE:
            if self._build_state == self.ADDING_POPULATIONS:
                raise ValueError("Must add at least one sample individual")
            elif self._build_state == self.ADDING_SAMPLES:
                self._individuals_writer.flush()
                self._samples_writer.flush()
            elif self._build_state == self.ADDING_SITES:
                self._sites_writer.flush()
            if self.num_sites == 0:
                raise ValueError("Must add at least one site")
            self._build_state = -1
            if self.sequence_length == 0:
                # Need to be careful that sequence_length is JSON serialisable here.
                self.data.attrs["sequence_length"] = float(self._last_position) + 1

        super().finalise()

    def __insert_individuals(self, other, pop_id_map=None):
        """
        Helper function to insert all the individuals in this SampleData file
        into the other. If pop_id_map is specified, use it to map
        population IDs in this dataset to IDs in other.
        """
        if pop_id_map is None:
            pop_id_map = {j: j for j in range(other.num_populations)}
            pop_id_map[tskit.NULL] = tskit.NULL
        for individual in other.individuals():
            self.add_individual(
                location=individual.location,
                metadata=individual.metadata,
                time=individual.time,
                flags=individual.flags,
                # We're assuming this is the same for all samples
                population=pop_id_map[individual.population],
                ploidy=len(individual.samples),
            )

    ####################################
    # Read mode
    ####################################

    def merge(self, other, **kwargs):
        """
        Returns a copy of this SampleData file merged with the specified
        other SampleData file. Subsequent keyword arguments are passed
        to the SampleData constructor for the returned merged dataset.

        The datasets are merged by following process:

        1. We add the populations from this dataset to the result, followed
           by the populations from other. Population references from the two
           datasets are updated accordingly.
        2. We add individual data from this dataset to the result, followed
           by the individuals from the other dataset.
        3. We merge the variant data from the two datasets by comparing sites
           by their position. If two sites in the datasets have the same
           position we combine the genotype data. The alleles from this dataset
           are updated to include any new alleles in other, and we then combine
           and update the genotypes accordingly. It is an error if sites with
           the same position have different ancestral state, time, or metadata
           values. For sites that exist in one dataset and not the other,
           we insert the site with MISSING_DATA present in the genotypes for
           the dataset that does not contain the site.
        4. We add the provenances for this dataset, followed by the provenances
           for the other dataset.

        :param SampleData other: The other :class:`SampleData` instance to
            to merge.
        :return: A new SampleData instance which contains the merged data
            from the two datasets.
        :rtype: .SampleData
        """
        if self.sequence_length != other.sequence_length:
            raise ValueError("Sample data files must have the same sequence length")
        with SampleData(sequence_length=self.sequence_length, **kwargs) as result:
            # Keep the same population IDs from self.
            for population in self.populations():
                result.add_population(population.metadata)
            # TODO we could avoid duplicate populations here by keying on the
            # metadata. It's slightly complicated by the case where the
            # metadata is all empty, but we could fall through to just
            # adding in all the populations as is, then.
            other_pop_map = {-1: -1}
            for population in other.populations():
                pid = result.add_population(population.metadata)
                other_pop_map[population.id] = pid

            result.__insert_individuals(self)
            result.__insert_individuals(other, other_pop_map)

            for variant in merge_variants(self, other):
                result.add_site(
                    position=variant.site.position,
                    genotypes=variant.genotypes,
                    alleles=variant.alleles,
                    metadata=variant.site.metadata,
                    time=variant.site.time,
                )

            for timestamp, record in list(self.provenances()) + list(
                other.provenances()
            ):
                result.add_provenance(timestamp, record)
            result.record_provenance(command="merge", **kwargs)
        return result

    def sites(self, ids=None):
        """
        Returns an iterator over the Site objects. A subset of the
        sites can be returned using the ``ids`` parameter. This must
        be a list of integer site IDs.
        """
        position = self.sites_position[:]
        alleles = self.sites_alleles[:]
        metadata = self.sites_metadata[:]
        time = self.sites_time[:]
        if ids is None:
            ids = np.arange(0, self.num_sites, dtype=int)
        for j in ids:
            site = Site(
                id=j,
                position=position[j],
                ancestral_state=alleles[j][0],
                alleles=tuple(alleles[j]),
                metadata=metadata[j],
                time=time[j],
            )
            yield site

    def num_alleles(self, sites=None):
        """
        Returns a numpy array of the number of alleles at each site. Missing data is
        not counted as an allele.

        :param array sites: A numpy array of sites for which to return data. If None
            (default) return all sites.

        :return: A numpy array of the number of alleles at each site.
        :rtype: numpy.ndarray(dtype=uint32)
        """
        if sites is None:
            sites = np.arange(self.num_sites)
        alleles = self.sites_alleles[:]
        num_alleles = np.zeros(self.num_sites, dtype=np.uint32)
        for j, alleles in enumerate(alleles):
            num_alleles[j] = len(alleles)
            if alleles[-1] is None:
                num_alleles[j] -= 1
        return num_alleles[sites]

    def variants(self, sites=None):
        """
        Returns an iterator over the Variant objects. This is equivalent to
        the TreeSequence.variants iterator.
        """
        all_genotypes = chunk_iterator(self.sites_genotypes, indexes=sites)
        for genotypes, site in zip(all_genotypes, self.sites(ids=sites)):
            yield Variant(site=site, alleles=site.alleles, genotypes=genotypes)

    def __all_haplotypes(self, sites=None):
        # We iterate over chunks vertically here, and it's not worth complicating
        # the chunk iterator to handle this.
        chunk_size = self.sites_genotypes.chunks[1]
        for j in range(self.num_samples):
            if j % chunk_size == 0:
                chunk = self.sites_genotypes[:, j : j + chunk_size].T
            a = chunk[j % chunk_size]
            yield j, a if sites is None else a[sites]

    def haplotypes(self, samples=None, sites=None):
        """
        Returns an iterator over the (sample_id, haplotype) pairs.

        :param list samples: The sample IDs for which haplotypes are returned. If
            ``None``, return haplotypes for all sample nodes, otherwise this may be a
            numpy array (or array-like) object (converted to dtype=np.int32).
        :param array sites: A numpy array of sites to use.
        """
        if samples is None:
            samples = np.arange(self.num_samples)
        else:
            samples = tskit.util.safe_np_int_cast(samples, dtype=np.int32)
            if np.any(samples[:-1] >= samples[1:]):
                raise ValueError("sample indexes must be in increasing order.")
            if samples.shape[0] > 0 and samples[-1] >= self.num_samples:
                raise ValueError("Sample index too large.")
        j = 0
        for index, a in self.__all_haplotypes(sites):
            if j == len(samples):
                break
            if index == samples[j]:
                yield index, a
                j += 1

    def individual(self, id_):
        # TODO document
        samples = np.where(self.samples_individual[:] == id_)[0]
        # Make sure the numpy arrays are converted to lists so that
        # we can compare individuals using ==
        return Individual(
            id_,
            location=list(self.individuals_location[id_]),
            metadata=self.individuals_metadata[id_],
            time=self.individuals_time[id_],
            population=self.individuals_population[id_],
            samples=list(samples),
            flags=self.individuals_flags[id_],
        )

    def individuals(self):
        individual_samples = [[] for _ in range(self.num_individuals)]
        for sample_id, individual_id in enumerate(self.samples_individual[:]):
            individual_samples[individual_id].append(sample_id)
        # TODO document
        iterator = zip(
            self.individuals_location[:],
            self.individuals_metadata[:],
            self.individuals_time[:],
            self.individuals_population[:],
            self.individuals_flags[:],
        )
        for j, (location, metadata, time, population, flags) in enumerate(iterator):
            yield Individual(
                j,
                location=list(location),
                metadata=metadata,
                time=time,
                population=population,
                samples=individual_samples[j],
                flags=flags,
            )

    def sample(self, id_):
        # TODO document
        return Sample(
            id_,
            individual=self.samples_individual[id_],
        )

    def samples(self):
        # TODO document
        iterator = self.samples_individual[:]
        for j, individual in enumerate(iterator):
            yield Sample(j, individual=individual)

    def population(self, id_):
        # TODO document
        return Population(id_, metadata=self.populations_metadata[id_])

    def populations(self):
        # TODO document
        iterator = self.populations_metadata[:]
        for j, metadata in enumerate(iterator):
            yield Population(j, metadata=metadata)


@attr.s
class Ancestor:
    """
    An ancestor object.
    """

    # TODO document properly.
    id = attr.ib()
    start = attr.ib()
    end = attr.ib()
    time = attr.ib()
    focal_sites = attr.ib()
    haplotype = attr.ib()


class AncestorData(DataContainer):
    """
    AncestorData(sample_data, *, path=None, num_flush_threads=0, compressor=None, \
    chunk_size=1024, max_file_size=None)

    Class representing the stored ancestor data produced by
    :func:`generate_ancestors`. See the ancestor data file format
    :ref:`specifications <sec_file_formats_ancestors>` for details on the structure
    of this file.

    See the documentation for :class:`SampleData` for a discussion of the
    ``max_file_size`` parameter.

    :param SampleData sample_data: The :class:`.SampleData` instance
        that this ancestor data file was generated from.
    :param str path: The path of the file to store the ancestor data. If None,
        the information is stored in memory and not persistent.
    :param int num_flush_threads: The number of background threads to use
        for compressing data and flushing to disc. If <= 0, do not spawn
        any threads but use a synchronous algorithm instead. Default=0.
    :param numcodecs.abc.Codec compressor: A :class:`numcodecs.abc.Codec`
        instance to use for compressing data. Any codec may be used, but
        problems may occur with very large datasets on certain codecs as
        they cannot compress buffers >2GB. If None, do not use any compression.
        Default=:class:`numcodecs.zstd.Zstd`.
    :param int chunk_size: The chunk size used for
        `zarr arrays <http://zarr.readthedocs.io/>`_. This affects
        compression level and algorithm performance. Default=1024.
    :param int max_file_size: If a file is being used to store this data, set
        a maximum size in bytes for the stored file. If None, the default
        value of 1GiB is used on Windows and 1TiB on other
        platforms (see above for details).
    """

    FORMAT_NAME = "tsinfer-ancestor-data"
    FORMAT_VERSION = (3, 0)

    def __init__(self, sample_data, **kwargs):
        super().__init__(**kwargs)
        sample_data._check_finalised()
        self.sample_data = sample_data
        self.data.attrs["sample_data_uuid"] = sample_data.uuid
        if self.sample_data.sequence_length == 0:
            raise ValueError("Bad samples file: sequence_length cannot be zero")
        self.data.attrs["sequence_length"] = self.sample_data.sequence_length
        self._last_time = 0

        chunks = self._chunk_size

        # By default all sites in the sample data file are used.
        self._num_alleles = self.sample_data.num_alleles()
        position = self.sample_data.sites_position[:]
        self.data.create_dataset(
            "sites/position",
            data=position,
            shape=position.shape,
            compressor=self._compressor,
            dtype=np.float64,
        )
        self.data.create_dataset(
            "ancestors/start",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.int32,
        )
        self.data.create_dataset(
            "ancestors/end",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.int32,
        )
        self.data.create_dataset(
            "ancestors/time",
            shape=(0,),
            chunks=chunks,
            compressor=self._compressor,
            dtype=np.float64,
        )
        self.data.create_dataset(
            "ancestors/focal_sites",
            shape=(0,),
            chunks=chunks,
            dtype="array:i4",
            compressor=self._compressor,
        )
        self.data.create_dataset(
            "ancestors/haplotype",
            shape=(0,),
            chunks=chunks,
            dtype="array:i1",
            compressor=self._compressor,
        )

        self._alloc_ancestor_writer()

        # Add in the provenance trail from the sample_data file.
        for timestamp, record in sample_data.provenances():
            self.add_provenance(timestamp, record)

    def _alloc_ancestor_writer(self):
        self.ancestor_writer = BufferedItemWriter(
            {
                "start": self.ancestors_start,
                "end": self.ancestors_end,
                "time": self.ancestors_time,
                "focal_sites": self.ancestors_focal_sites,
                "haplotype": self.ancestors_haplotype,
            },
            num_threads=self._num_flush_threads,
        )

    def summary(self):
        return "AncestorData(num_ancestors={}, num_sites={})".format(
            self.num_ancestors, self.num_sites
        )

    def __str__(self):
        values = [
            ("sequence_length", self.sequence_length),
            ("sample_data_uuid", self.sample_data_uuid),
            ("num_ancestors", self.num_ancestors),
            ("num_sites", self.num_sites),
            ("sites/position", zarr_summary(self.sites_position)),
            ("ancestors/start", zarr_summary(self.ancestors_start)),
            ("ancestors/end", zarr_summary(self.ancestors_end)),
            ("ancestors/time", zarr_summary(self.ancestors_time)),
            ("ancestors/focal_sites", zarr_summary(self.ancestors_focal_sites)),
            ("ancestors/haplotype", zarr_summary(self.ancestors_haplotype)),
        ]
        return super().__str__() + self._format_str(values)

    def data_equal(self, other):
        """
        Returns True if all the data attributes of this input file and the
        specified input file are equal. This compares every attribute except
        the UUID.
        """
        return (
            self.sequence_length == other.sequence_length
            and self.sample_data_uuid == other.sample_data_uuid
            and self.format_name == other.format_name
            and self.format_version == other.format_version
            and self.num_ancestors == other.num_ancestors
            and self.num_sites == other.num_sites
            and np.array_equal(self.sites_position[:], other.sites_position[:])
            and np.array_equal(self.ancestors_start[:], other.ancestors_start[:])
            and np.array_equal(self.ancestors_end[:], other.ancestors_end[:])
            # Need to take a different approach with np object arrays.
            and np_obj_equal(
                self.ancestors_focal_sites[:], other.ancestors_focal_sites[:]
            )
            and np_obj_equal(self.ancestors_haplotype[:], other.ancestors_haplotype[:])
        )

    @property
    def sequence_length(self):
        return self.data.attrs["sequence_length"]

    @property
    def sample_data_uuid(self):
        return self.data.attrs["sample_data_uuid"]

    @property
    def num_ancestors(self):
        return self.ancestors_start.shape[0]

    @property
    def num_sites(self):
        return self.sites_position.shape[0]

    @property
    def sites_position(self):
        return self.data["sites/position"]

    @property
    def ancestors_start(self):
        return self.data["ancestors/start"]

    @property
    def ancestors_end(self):
        return self.data["ancestors/end"]

    @property
    def ancestors_time(self):
        return self.data["ancestors/time"]

    @property
    def ancestors_focal_sites(self):
        return self.data["ancestors/focal_sites"]

    @property
    def ancestors_haplotype(self):
        return self.data["ancestors/haplotype"]

    @property
    def ancestors_length(self):
        """
        Returns the length of ancestors in physical coordinates.
        """
        # Ancestor start and end are half-closed. The last site is assumed
        # to cover the region up to sequence length.
        pos = np.hstack([self.sites_position[:], [self.sequence_length]])
        start = self.ancestors_start[:]
        end = self.ancestors_end[:]
        return pos[end] - pos[start]

    def insert_proxy_samples(
        self,
        sample_data,
        *,
        sample_ids=None,
        epsilon=None,
        allow_mutation=False,
        require_same_sample_data=True,
        **kwargs,
    ):
        """
        Take a set of samples from a ``sample_data`` instance and create additional
        "proxy sample ancestors" from them, returning a new :class:`.AncestorData`
        instance including both the current ancestors and the additional ancestors
        at the appropriate time points.

        A *proxy sample ancestor* is an ancestor based upon a known sample. At
        sites used in the full inference process, the haplotype of this ancestor
        is identical to that of the sample on which it is based. The time of the
        ancestor is taken to be a fraction ``epsilon`` older than the sample on
        which it is based.

        A common use of this function is to provide ancestral nodes for anchoring
        historical samples at the correct time when matching them into a tree
        sequence during the :func:`tsinfer.match_samples` stage of inference.
        For this reason, by default, the samples chosen from ``sample_data``
        are those associated with historical (i.e. non-contemporary)
        :ref:`individuals <sec_inference_data_model_individual>`. This can be
        altered by using the ``sample_ids`` parameter.

        .. note::

            The proxy sample ancestors inserted here will correspond to extra nodes
            in the inferred tree sequence. At sites which are not used in the full
            inference process (e.g. sites unique to a single historical sample),
            these proxy sample ancestor nodes may have a different genotype from
            their corresponding sample.

        :param SampleData sample_data: The :class:`.SampleData` instance
            from which to select the samples used to create extra ancestors.
        :param list(int) sample_ids: A list of sample ids in the ``sample_data``
            instance that will be selected to create the extra ancestors. If
            ``None`` (default) select all the historical samples, i.e. those
            associated with an :ref:`sec_inference_data_model_individual` whose
            time is greater than zero. The order of ids is ignored, as are
            duplicate ids.
        :param list(float) epsilon: An list of small time increments
            determining how much older each proxy sample ancestor is than the
            corresponding sample listed in ``sample_ids``. A single value is also
            allowed, in which case it is used as the time increment for all selected
            proxy sample ancestors. If None (default) find :math:`{\\delta}t`, the
            smallest time difference between between the sample times and the next
            oldest ancestor in the current :class:`.AncestorData` instance, setting
            ``epsilon`` = :math:`{\\delta}t / 100` (or, if all selected samples
            are at least as old as the oldest ancestor, take :math:`{\\delta}t`
            to be the smallest non-zero time difference between existing ancestors).
        :param bool allow_mutation: If ``False`` (the default), any site in a proxy
            sample ancestor that has a derived allele must have a pre-existing
            mutation in an older (non-proxy) ancestor, otherwise an error is raised.
            Alternatively, if ``allow_mutation`` is ``True``, proxy ancestors can
            contain a de-novo mutation at a site that also has a mutation elsewhere
            (i.e. breaking the infinite sites assumption), allowing them to possess
            derived alleles at sites where there are no pre-existing mutations in
            older ancestors.
        :param bool require_same_sample_data: If ``True`` (default) then the
            the ``sample_data`` parameter must point to the same :class:`.SampleData`
            instance as that used to generate the current ancestors. If ``False``,
            this requirement is not enforced, and it is the user's responsibility
            to ensure that the encoding of alleles in ``sample_data`` matches the
            encoding in the current :class:`AncestorData` instance (i.e. that in the
            original :class:`.SampleData` instance on which the current ancestors
            are based).
        :param \\**kwargs: Further arguments passed to the constructor when creating
            the new :class:`AncestorData` instance which will be returned.

        :return: A new :class:`.AncestorData` object.
        :rtype: AncestorData
        """
        self._check_finalised()
        sample_data._check_finalised()
        if require_same_sample_data:
            if sample_data.uuid != self.sample_data_uuid:
                raise ValueError(
                    "sample_data differs from that used to build the initial ancestors"
                )
        if self.sequence_length != sample_data.sequence_length:
            raise ValueError("sample_data does not have the correct sequence length")
        used_sites = np.isin(sample_data.sites_position[:], self.sites_position[:])
        if np.sum(used_sites) != self.num_sites:
            raise ValueError("Genome positions in ancestors missing from sample_data")

        if sample_ids is None:
            sample_ids = []
            for i in sample_data.individuals():
                if i.time > 0:
                    sample_ids += i.samples
        # sort by ID and make unique for quick haplotype access
        sample_ids, unique_indices = np.unique(np.array(sample_ids), return_index=True)

        sample_times = np.zeros(len(sample_ids), dtype=self.ancestors_time.dtype)
        for i, s in enumerate(sample_ids):
            sample = sample_data.sample(s)
            if sample.individual != tskit.NULL:
                sample_times[i] = sample_data.individual(sample.individual).time

        if epsilon is not None:
            epsilons = np.atleast_1d(epsilon)
            if len(epsilons) == 1:
                # all get the same epsilon
                epsilons = np.repeat(epsilons, len(sample_ids))
            else:
                if len(epsilons) != len(unique_indices):
                    raise ValueError(
                        "The number of epsilon values must equal the number of "
                        f"sample_ids ({len(sample_ids)})"
                    )
                epsilons = epsilons[unique_indices]

        else:
            anc_times = self.ancestors_time[:][::-1]  # find ascending time order
            older_index = np.searchsorted(anc_times, sample_times, side="right")
            # Don't include times older than the oldest ancestor
            allowed = older_index < self.num_ancestors
            if np.sum(allowed) > 0:
                delta_t = anc_times[older_index[allowed]] - sample_times[allowed]
            else:
                # All samples have times equal to or older than the oldest curr ancestor
                time_diffs = np.diff(anc_times)
                delta_t = np.min(time_diffs[time_diffs > 0])
            epsilons = np.repeat(np.min(delta_t) / 100.0, len(sample_ids))

        proxy_times = sample_times + epsilons
        reverse_time_sorted_indexes = np.argsort(proxy_times)[::-1]
        # In cases where we have more than a handful of samples to use as proxies, it is
        # inefficient to access the haplotypes out of order, so we iterate and cache
        # (caution: the haplotypes list may be quite large in this case)
        haplotypes = [
            h[1] for h in sample_data.haplotypes(samples=sample_ids, sites=used_sites)
        ]

        with AncestorData(sample_data, **kwargs) as other:
            other.set_inference_sites(used_sites)
            mutated_sites = set()  # To check if mutations have ocurred yet
            ancestors_iter = self.ancestors()
            ancestor = next(ancestors_iter, None)
            for i in reverse_time_sorted_indexes:
                proxy_time = proxy_times[i]
                sample_id = sample_ids[i]
                haplotype = haplotypes[i]
                while ancestor is not None and ancestor.time > proxy_time:
                    other.add_ancestor(**attr.asdict(ancestor, filter=exclude_id))
                    mutated_sites.update(ancestor.focal_sites)
                    ancestor = next(ancestors_iter, None)
                if not allow_mutation:
                    derived_sites = set(np.where(haplotype > 0)[0])
                    if not derived_sites.issubset(mutated_sites):
                        raise ValueError(
                            f"Sample {sample_id} contains a new derived allele, which "
                            "requires a novel mutation, but `allow_mutation` is False."
                        )
                logger.debug(
                    f"Inserting proxy ancestor: sample {sample_id} at time {proxy_time}"
                )
                other.add_ancestor(
                    start=0,
                    end=self.num_sites,
                    time=proxy_time,
                    focal_sites=[],
                    haplotype=haplotype,
                )
            # Add any ancestors remaining in the current instance
            while ancestor is not None:
                other.add_ancestor(**attr.asdict(ancestor, filter=exclude_id))
                ancestor = next(ancestors_iter, None)

            # TODO - set metadata on these ancestors, once ancestors have metadata
            other.clear_provenances()
            for timestamp, record in self.provenances():
                other.add_provenance(timestamp, record)
            if sample_data.uuid != self.sample_data_uuid:
                pass  # TODO: if sample files don't match, we need extra provenance info
            other.record_provenance(command="insert_proxy_samples", **kwargs)

        assert other.num_ancestors == self.num_ancestors + len(sample_ids)
        return other

    ####################################
    # Write mode (building and editing)
    ####################################

    def set_inference_sites(self, site_ids):
        """
        Sets the sites used for inference (i.e., the sites at which ancestor haplotypes
        are defined) to the specified list of site IDs. This must be a subset of the
        sites in the sample data file, and the IDs must be in increasing order.

        This must be called before the first call to :meth:`.add_ancestor`.
        """
        self._check_build_mode()
        position = self.sample_data.sites_position[:][site_ids]
        array = self.data["sites/position"]
        array.resize(position.shape)
        array[:] = position
        self._num_alleles = self.sample_data.num_alleles(site_ids)

    def add_ancestor(self, start, end, time, focal_sites, haplotype):
        """
        Adds an ancestor with the specified haplotype, with ancestral material over the
        interval [start:end], that is associated with the specified timepoint and has new
        mutations at the specified list of focal sites. Ancestors should be added in time
        order, with the oldest first. The id of the added ancestor is returned.
        """
        self._check_build_mode()
        haplotype = tskit.util.safe_np_int_cast(haplotype, dtype=np.int8, copy=True)
        focal_sites = tskit.util.safe_np_int_cast(
            focal_sites, dtype=np.int32, copy=True
        )
        if start < 0:
            raise ValueError("Start must be >= 0")
        if end > self.num_sites:
            raise ValueError("end must be <= num_sites")
        if start >= end:
            raise ValueError("start must be < end")
        if haplotype.shape != (end - start,):
            raise ValueError("haplotypes incorrect shape.")
        if np.any(haplotype >= self._num_alleles[start:end]):
            raise ValueError("haplotype values must be < num_alleles.")
        if np.any(focal_sites < start) or np.any(focal_sites >= end):
            raise ValueError("focal sites must be between start and end")
        if time <= 0:
            raise ValueError("time must be > 0")
        if self._last_time != 0 and time > self._last_time:
            raise ValueError("older ancestors must be added before younger ones")
        self._last_time = time
        return self.ancestor_writer.add(
            start=start,
            end=end,
            time=time,
            focal_sites=focal_sites,
            haplotype=haplotype,
        )

    def finalise(self):
        if self._mode == self.BUILD_MODE:
            self.ancestor_writer.flush()
            self.ancestor_writer = None
        super().finalise()

    ####################################
    # Read mode
    ####################################

    def ancestors(self):
        """
        Returns an iterator over all the ancestors.
        """
        # TODO document properly.
        start = self.ancestors_start[:]
        end = self.ancestors_end[:]
        time = self.ancestors_time[:]
        focal_sites = self.ancestors_focal_sites[:]
        for j, h in enumerate(chunk_iterator(self.ancestors_haplotype)):
            yield Ancestor(
                id=j,
                start=start[j],
                end=end[j],
                time=time[j],
                focal_sites=focal_sites[j],
                haplotype=h,
            )


def load(path):
    """
    Loads a tsinfer :class:`.SampleData` or :class:`.AncestorData` file from
    the specified path. The correct class will be determined by the content
    of the file. If the file is format not recognised a
    :class:`.FileFormatError` will be thrown.

    :param str path: The path of the file we wish to load.
    :return: The corresponding :class:`.SampleData` or :class:`.AncestorData`
        instance opened in read only mode.
    :rtype: :class:`.AncestorData` or :class:`.SampleData`.
    :raises: :class:`.FileFormatError` if the file cannot be read.
    """
    # TODO This is pretty inelegant, but it works. Really we should call the
    # load on the superclass which can dispatch to the registered subclasses
    # for a given format_name.
    tsinfer_file = None
    try:
        logger.debug("Trying SampleData file")
        tsinfer_file = SampleData.load(path)
        logger.debug("Loaded SampleData file")
    except exceptions.FileFormatError as e:
        logger.debug(f"SampleData load failed: {e}")
    try:
        logger.debug("Trying AncestorData file")
        tsinfer_file = AncestorData.load(path)
        logger.debug("Loaded AncestorData file")
    except exceptions.FileFormatError as e:
        logger.debug(f"AncestorData load failed: {e}")
    if tsinfer_file is None:
        raise exceptions.FileFormatError(
            "Unrecognised file format. Try running with -vv and check the log "
            "for more details on what went wrong"
        )
    return tsinfer_file
