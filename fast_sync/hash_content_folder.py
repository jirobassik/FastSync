import multiprocessing
from hashlib import md5
from itertools import chain
from pathlib import Path, PosixPath

from .config_worker import get_ext

class HashContentFolder:
    def create_hash(self, pure_path: Path):
        with multiprocessing.Pool() as pool:
            iter_hashes = pool.map(
                self._hash_path, self._rglob_filter_pattern_files(pure_path)
            )
        return iter_hashes

    @staticmethod
    def _hash_path(byte_file: PosixPath):
        return md5(byte_file.read_bytes()).hexdigest(), byte_file

    @staticmethod
    def _rglob_filter_pattern_files(pure_path: Path):
        return chain.from_iterable(
            pure_path.rglob(pattern) for pattern in get_ext()
        )  # TODO Настройка фильтра расширений (через томл или на ввод через аргуумент)
