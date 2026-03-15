from enum import Enum
from typing import Type

from fast_sync.containers import Container


class Readers(Enum):
    SIMPLE = "simple_reader"
    FILTER = "filter_reader"


class Hashes(Enum):
    SIMPLE = "simple_hash_progressbar"
    CACHE = "cache_hash_progressbar"


def reader_configure(
    fast_sync_container: Type[Container], extensions: tuple, folders: tuple
):
    if extensions or folders:
        fast_sync_container.filter_extensions.set_args(*extensions)
        fast_sync_container.filter_folder.set_args(*folders)
        return Readers.FILTER
    return Readers.SIMPLE


def hash_configure(hashing: bool):
    if hashing:
        return Hashes.CACHE

    return Hashes.SIMPLE
