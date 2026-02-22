from pathlib import Path

from diskcache import Cache

from fast_sync import FolderFilterReader, FolderReader
from fast_sync.hash_content_folder import HashContentFolder

from .cache_folder_creation import CacheFolderCreation


class HashContentFolderCaching(HashContentFolder):
    def __init__(
        self,
        reader: FolderReader | FolderFilterReader = FolderReader(),
        cache_path: CacheFolderCreation = CacheFolderCreation(),
    ):
        super().__init__(reader)
        self._cache_path = Cache(cache_path.path_to_cache.as_posix())

    def _hash_path(self, path_to_file: Path, path_to_main_folder: Path):
        filename_without_parent_as_posix = path_to_file.relative_to(
            path_to_main_folder
        ).as_posix()
        if filename_without_parent_as_posix not in self._cache_path:
            key, _ = super()._hash_path(path_to_file, path_to_main_folder)
            self._cache_path.set(key=filename_without_parent_as_posix, value=key)
            return key, path_to_file
        else:
            return self._cache_path.get(filename_without_parent_as_posix), path_to_file
