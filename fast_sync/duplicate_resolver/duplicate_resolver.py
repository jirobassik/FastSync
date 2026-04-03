from pathlib import Path
from typing import ValuesView

from loguru import logger
from send2trash import send2trash

from fast_sync.duplicate_resolver.duplicate_finder import EqualFinderGroupByHash
from fast_sync.duplicate_resolver.duplicate_questions.main_question import (
    EqualMethodQuestion,
)
from fast_sync.hash_content_folder.hash_content_folder import HashContentFolder
from fast_sync.hash_content_folder.hash_content_folder_caching.hash_content_folder_caching import (
    HashContentFolderCaching,
)
from fast_sync.utils.errors import EqualResolverError
from fast_sync.utils.path_setup import ValidPath


class EqualValidation:
    @staticmethod
    def validate(equal_el):
        if not equal_el:
            raise EqualResolverError("Not found equal elements")


class EqualResolver(EqualValidation):
    path = ValidPath()

    __slots__ = ["_hash_method", "_equal_finder", "_questions"]

    def __init__(
        self,
        hash_method: HashContentFolder | HashContentFolderCaching = HashContentFolder(),
    ):
        self._hash_method = hash_method
        self._equal_finder = EqualFinderGroupByHash()
        self._questions = EqualMethodQuestion()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(hash_method={self._hash_method},"
            f"equal_finder={self._equal_finder},"
            f"questions={self._questions})"
        )

    def path_setup(self, path: str | Path):
        self.path = path

    def get_equal_elements(self) -> ValuesView[list[Path]]:
        calculate_hash = self._hash_method.create_hash(self.path)
        equal_el = self._equal_finder.find_equal(calculate_hash)

        self.validate(equal_el)
        return equal_el

    def equal_resolver(self):
        equal_el = self.get_equal_elements()

        dublicates_from_user = self._questions.start_questions(equal_el)
        for file_to_delete in dublicates_from_user:
            self.delete_file(file_to_delete)

    @staticmethod
    def delete_file(path_to_file: Path):
        logger.info(f"File: {path_to_file} has been deleted")
        send2trash(path_to_file)
