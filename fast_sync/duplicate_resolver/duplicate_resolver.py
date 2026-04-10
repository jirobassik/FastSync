from pathlib import Path
from typing import ValuesView

from loguru import logger
from send2trash import send2trash

from fast_sync.duplicate_resolver.duplicate_filtering import (
    FilterDuplicateBase,
    FilterDuplicateByDateCreationTime,
)
from fast_sync.duplicate_resolver.duplicate_finder import DuplicateFinderGroupByHash
from fast_sync.hash_content_folder.hash_content_folder import HashContentFolder
from fast_sync.hash_content_folder.hash_content_folder_caching.hash_content_folder_caching import (
    HashContentFolderCaching,
)
from fast_sync.utils.errors import EqualResolverError
from fast_sync.utils.path_setup import ValidPath


class DuplicatesFileValidation:
    @staticmethod
    def validate(duplicates: ValuesView[list[Path]]):
        if not duplicates:
            raise EqualResolverError("Not found duplicate files")


class DuplicateResolver(DuplicatesFileValidation):
    path = ValidPath()

    __slots__ = ["_hashing_content", "_find_duplicates", "_filter_duplicates"]

    def __init__(
        self,
        hashing_content: HashContentFolder
        | HashContentFolderCaching = HashContentFolder(),
        filter_duplicates: FilterDuplicateBase = FilterDuplicateByDateCreationTime,
    ):
        self._hashing_content = hashing_content
        self._filter_duplicates = filter_duplicates
        self._find_duplicates = DuplicateFinderGroupByHash()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(hashing_content={self._hashing_content},"
            f"filter_duplicates={self._filter_duplicates},"
            f"find_duplicates={self._find_duplicates})"
        )

    def path_setup(self, path: str | Path):
        self.path = path

    def get_duplicate_elements(self) -> ValuesView[list[Path]]:
        calculate_hash = self._hashing_content.create_hash(self.path)
        duplicates = self._find_duplicates.find_duplicate(calculate_hash)

        self.validate(duplicates)
        return duplicates

    def resolve(self):
        equal_el = self.get_duplicate_elements()

        filters_duplicates = self._filter_duplicates.filter_duplicate(equal_el)

        for file_to_delete in filters_duplicates:
            self._delete_file(file_to_delete)

    @staticmethod
    def _delete_file(path_to_file: Path):
        send2trash(path_to_file)
        logger.debug(f"File: {path_to_file} has been deleted")
