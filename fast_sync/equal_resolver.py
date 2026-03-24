from pathlib import Path

import inquirer
from loguru import logger

from fast_sync.hash_content_folder.hash_content_folder import HashContentFolder
from fast_sync.hash_content_folder.hash_content_folder_caching.hash_content_folder_caching import (
    HashContentFolderCaching,
)
from fast_sync.utils.path_setup import ValidPath
from fast_sync.utils.types import ListHashPathKeyValue


class EqualResolver:
    path = ValidPath()

    def __init__(
        self,
        hash_method: HashContentFolder | HashContentFolderCaching = HashContentFolder(),
    ):
        self._hash_method = hash_method
        self._equal_finder = EqualFinder()

    def path_setup(self, path: str | Path):
        self.path = path

    def equal_resolver(self):
        calculate_hash = self._hash_method.create_hash(self.path)
        equal_el = self._equal_finder.find_equal(calculate_hash)
        dublicates_from_user = equal_question(equal_el)

        for answer in dublicates_from_user:
            self.delete_file(answer)

    @staticmethod
    def delete_file(path_to_file: Path):
        logger.info(f"File: {path_to_file} has been deleted")
        path_to_file.unlink(missing_ok=True)


class EqualFinder:
    def __init__(self, only_name=False):
        self._path_attr = self.path_setupper(only_name)

    def find_equal(self, folder_hash_structure: ListHashPathKeyValue):
        equal_files_paths = []
        dublicates_hashes = self._find_dublicates_hashes(folder_hash_structure)
        for hash_path_path in folder_hash_structure:
            if hash_path_path[0][0] in dublicates_hashes:
                equal_files_paths.append(self._path_attr(hash_path_path[1]))
        logger.debug(f"Equal files: {equal_files_paths}")
        return equal_files_paths

    @staticmethod
    def _find_dublicates_hashes(folder_hash_structure: ListHashPathKeyValue):
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


def equal_question(dublicates: list) -> list:
    questions = [
        inquirer.Checkbox(
            "Equal files",
            message="Dublicates files. Choose to delete",
            choices=dublicates,
            carousel=True,
        ),
    ]

    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)
    logger.debug(f"Get from checkbox {answers}")
    return answers.get("Equal files")
