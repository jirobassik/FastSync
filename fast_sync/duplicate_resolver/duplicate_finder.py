from collections import defaultdict
from pathlib import Path
from typing import ValuesView

from loguru import logger

from fast_sync.utils.types import ListHashPathKeyValue


class DuplicateFinder:
    __slots__ = ["_path_attr"]

    def __init__(self, only_name=False):
        self._path_attr = self.path_setupper(only_name)

    def __repr__(self):
        return f"{self.__class__.__name__}(path_attr={self._path_attr}"

    def find_duplicate(self, folder_hash_structure: ListHashPathKeyValue) -> list[Path]:
        equal_files_paths = []
        dublicates_hashes = self._find_dublicates_hashes(folder_hash_structure)

        for hash_path_path in folder_hash_structure:
            if hash_path_path[0][0] in dublicates_hashes:
                equal_files_paths.append(self._path_attr(hash_path_path[1]))
        logger.debug(f"Equal files: {equal_files_paths}")
        return equal_files_paths

    @staticmethod
    def _find_dublicates_hashes(
        folder_hash_structure: ListHashPathKeyValue,
    ) -> set[str]:
        dublicates = set()
        seen = set()

        for hash_path_path in folder_hash_structure:
            file_hash = hash_path_path[0][0]
            if file_hash in seen:
                dublicates.add(file_hash)
            else:
                seen.add(file_hash)
        logger.debug(f"Dublicates hashes: {dublicates}")
        return dublicates

    @staticmethod
    def path_setupper(only_name):

        def _path_setupper(path: Path):
            if only_name:
                return path.name
            return path

        return _path_setupper


class DuplicateFinderGroupByHash(DuplicateFinder):
    def find_duplicate(
        self, folder_hash_structure: ListHashPathKeyValue
    ) -> ValuesView[list[Path]]:
        grouped_by_hash = defaultdict(list)
        dublicates_hashes = self._find_dublicates_hashes(folder_hash_structure)

        for hash_path_path in folder_hash_structure:
            if hash_path_path[0][0] in dublicates_hashes:
                grouped_by_hash[hash_path_path[0][0]].append(
                    self._path_attr(hash_path_path[1])
                )
        logger.debug(f"Equal files: {grouped_by_hash}")
        return grouped_by_hash.values()
