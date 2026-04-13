from enum import Enum
from typing import Type

from fast_sync.containers.main_container import Container


class Readers(Enum):
    SIMPLE = "simple_reader"
    FILTER = "filter_reader"


class Hashes(Enum):
    SIMPLE = "simple_hash"
    CACHE = "cache_hash"


def reader_configure(
    fast_sync_container: Type[Container], extensions: tuple, folders: tuple
):
    if extensions or folders:
        fast_sync_container.reader.filter_extensions.set_args(*extensions)
        fast_sync_container.reader.filter_folder.set_args(*folders)
        return Readers.FILTER
    return Readers.SIMPLE


def hash_configure(
    fast_sync_container: Type[Container], caching: bool, num_processes: int
):
    if caching:
        fast_sync_container.hasher.hash_content_folder_caching.add_kwargs(
            num_processes=num_processes
        )
        return Hashes.CACHE
    fast_sync_container.hasher.hash_content_folder.add_kwargs(
        num_processes=num_processes
    )
    return Hashes.SIMPLE
