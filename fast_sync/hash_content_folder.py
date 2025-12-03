import multiprocessing
from hashlib import md5
from itertools import chain
from pathlib import Path, PosixPath
from tqdm import tqdm


class HashContentFolder:
    # def create_hash(self, pure_path: Path):
    #     with multiprocessing.Pool() as pool:
    #         iter_hashes = pool.map(self._hash_path, self.__rglob_filter_pattern_files(pure_path))
    #     return iter_hashes

    def create_hash(self, pure_path: Path):
        results = []
        with multiprocessing.Pool() as pool:
            with tqdm(desc=f"Processing: {pure_path}") as pbar:
                for result in pool.imap_unordered(self._hash_path, self.__rglob_filter_pattern_files(pure_path)):
                    results.append(result)
                    pbar.update(1)
        return results

    @staticmethod
    def _hash_path(byte_file: PosixPath):
        return md5(byte_file.read_bytes()).hexdigest(), byte_file

    @staticmethod
    def __rglob_filter_pattern_files(pure_path: Path):
        return chain.from_iterable(pure_path.rglob(pattern)
                                   for pattern in ["*.mp3", "*.wav"])  # TODO Настройка фильтра расширений
