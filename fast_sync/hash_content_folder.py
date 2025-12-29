import multiprocessing
from hashlib import md5
from pathlib import Path

from fast_sync import FolderReader, FolderFilterReader


class HashContentFolder:
    __slots__ = ("_reader",)

    def __init__(self, reader: FolderReader | FolderFilterReader):
        self._reader = reader

    def create_hash(self, pure_path: Path) -> list[tuple[str, Path]]:
        with multiprocessing.Pool() as pool:
            iter_hashes = pool.map(
                self._hash_path, self._reader.operation(pure_path)
            )
        return iter_hashes

    @staticmethod
    def _hash_path(byte_file: Path) -> tuple[str, Path]:
        return md5(byte_file.read_bytes()).hexdigest(), byte_file
