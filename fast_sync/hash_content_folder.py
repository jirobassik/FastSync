import multiprocessing
from hashlib import md5
from pathlib import Path

from fast_sync import FolderReader, FolderFilterReader


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

    def _create_hash(self, pure_path: Path) -> list[tuple[str, Path]]:
        with multiprocessing.Pool() as pool:
            iter_hashes = pool.map(
                self._hash_path, self._reader.operation(pure_path)
            )
        return iter_hashes

    @staticmethod
    def _hash_path(byte_file: Path) -> tuple[str, Path]:
        return md5(byte_file.read_bytes()).hexdigest(), byte_file
