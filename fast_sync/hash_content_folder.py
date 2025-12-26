import multiprocessing
from hashlib import md5
from pathlib import Path, PosixPath


class HashContentFolder:
    def __init__(self, reader):
        self.reader = reader

    def create_hash(self, pure_path: Path):
        with multiprocessing.Pool() as pool:
            iter_hashes = pool.map(
                self._hash_path, self.reader.operation(pure_path)
            )
        return iter_hashes

    @staticmethod
    def _hash_path(byte_file: PosixPath):
        return md5(byte_file.read_bytes()).hexdigest(), byte_file
