import multiprocessing
from functools import partial
from hashlib import md5
from pathlib import Path

from fast_sync import FolderReader, FolderFilterReader
from fast_sync.utils.types import ListHashPathKeyValue, HashPathKeyValue


class HashValue:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]


class HashContentFolder:
    left_hash = HashValue()
    right_hash = HashValue()

    def __init__(self, reader: FolderReader | FolderFilterReader):
        self._reader = reader

    def calculate_hash(self, left_path: Path, right_path: Path):
        self.left_hash = self._create_hash(left_path)
        self.right_hash = self._create_hash(right_path)
        return self

    def _create_hash(self, path_to_main_folder: Path) -> ListHashPathKeyValue:
        with multiprocessing.Pool() as pool:
            hash_path_add_path_to_main_folder = partial(self._hash_path, path_to_main_folder=path_to_main_folder)
            iter_hashes = pool.map(
                hash_path_add_path_to_main_folder, self._reader.operation(path_to_main_folder)
            )
        return iter_hashes

    @staticmethod
    def _hash_path(path_to_file: Path, path_to_main_folder: Path) -> HashPathKeyValue:
        key = (md5(path_to_file.read_bytes()).hexdigest(), path_to_file.relative_to(path_to_main_folder))
        value = path_to_file
        return key, value
