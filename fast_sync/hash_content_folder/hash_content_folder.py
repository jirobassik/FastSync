import multiprocessing
from functools import partial
from hashlib import md5
from pathlib import Path
from typing import Self

from loguru import logger

from fast_sync import FolderFilterReader, FolderReader
from fast_sync.utils.custom_repr import hash_repr
from fast_sync.utils.errors import HashContentFolderError
from fast_sync.utils.types import HashPathKeyValue, ListHashPathKeyValue


class HashValue:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        try:
            return instance.__dict__[self._name]
        except KeyError:
            raise HashContentFolderError(
                message="The hash has not been calculated yet. Use `.calculate_hash`"
            )


class HashContentFolder:
    left_hash = HashValue()
    right_hash = HashValue()

    def __init__(self, reader: FolderReader | FolderFilterReader = FolderReader()):
        self._reader = reader

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(left_hash={hash_repr.repr_lazy_attr(self, 'left_hash')}, "
            f"right_hash={hash_repr.repr_lazy_attr(self, 'right_hash')}, "
            f"reader={self._reader})"
        )

    def calculate_hash(self, left_path: Path, right_path: Path) -> Self:
        self.left_hash = self._create_hash(left_path)
        self.right_hash = self._create_hash(right_path)
        return self

    def _create_hash(self, path_to_main_folder: Path) -> ListHashPathKeyValue:
        with multiprocessing.Pool() as pool:
            hash_path_add_path_to_main_folder = partial(
                self._hash_path,
                path_to_main_folder=path_to_main_folder,
            )
            iter_hashes = pool.map(
                hash_path_add_path_to_main_folder,
                self._reader.read(path_to_main_folder),
            )
        return iter_hashes

    @staticmethod
    def _hash_path(path_to_file: Path, path_to_main_folder: Path) -> HashPathKeyValue:
        try:
            key = (
                md5(path_to_file.read_bytes()).hexdigest(),
                path_to_file.relative_to(path_to_main_folder),
            )
        except PermissionError as error:
            logger.error(f"Permission denied: {error.filename}")
            raise HashContentFolderError(
                f"Cannot calculate hash at {error.filename}:{error.strerror}",
                error_class=error,
            )
        else:
            value = path_to_file
            return key, value
