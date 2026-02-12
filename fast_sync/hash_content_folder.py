import multiprocessing
import platform
from functools import partial
from hashlib import md5
from pathlib import Path

from diskcache import Cache

from fast_sync import FolderFilterReader, FolderReader
from fast_sync.utils.error import HashCalculationError
from fast_sync.utils.types import HashPathKeyValue, ListHashPathKeyValue


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
            hash_path_add_path_to_main_folder = partial(
                self._hash_path,
                path_to_main_folder=path_to_main_folder,
            )
            iter_hashes = pool.map(
                hash_path_add_path_to_main_folder,
                self._reader.operation(path_to_main_folder),
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
            raise HashCalculationError(error.filename)
        else:
            value = path_to_file
            return key, value


# class HashFolderCreation:
#     def __init__(self, path_to_folder=None):
#         if path_to_folder is None:
#             path_to_folder = self.resolve_path()
#         self.path_to_folder = path_to_folder
#
#     def resolve_path(self):
#         home_path = Path().home()
#         match platform.system():
#             case "Linux":
#                 path_to_cache = Path(home_path, ".cache")
#             case "Windows":
#                 path_to_cache = Path(home_path, "AppData", "Local")
#         if path_to_cache.exists()
#
#     def platform_system_resolve_path(self):
#         home_path = Path().home()
#         match platform.system():
#             case "Linux":
#                 path_to_cache = Path(home_path, ".cache")
#             case "Windows":
#                 path_to_cache = Path(home_path, "AppData", "Local")
#         if path_to_cache.exists()


class HashContentFolderCaching(HashContentFolder):
    def __init__(self, reader: FolderReader | FolderFilterReader):
        super().__init__(reader)
        match platform.system():
            case "Linux":
                path_to_cache = Path(Path().home(), ".cache", "FastSync")
            case "Windows":
                path_to_cache = Path(Path().home(), "AppData", "Local", "FastSync")
            case _:
                path_to_cache = Path(Path().home())
        path_to_cache.mkdir(exist_ok=True)
        if not path_to_cache.exists():
            raise ValueError
        self._cache_path = Cache(path_to_cache.as_posix())

    def _hash_path(self, path_to_file: Path, path_to_main_folder: Path):
        filename_without_parent_as_posix = path_to_file.relative_to(
            path_to_main_folder
        ).as_posix()
        if filename_without_parent_as_posix not in self._cache_path:
            key, _ = super()._hash_path(path_to_file, path_to_main_folder)
            self._cache_path.set(key=filename_without_parent_as_posix, value=key)
            return key, path_to_file
        else:
            return self._cache_path.get(filename_without_parent_as_posix), path_to_file
