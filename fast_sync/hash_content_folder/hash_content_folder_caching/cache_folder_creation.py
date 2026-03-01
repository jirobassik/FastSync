import platform
from enum import Enum
from pathlib import Path

from loguru import logger

from fast_sync.utils.errors import CacheFolderCreationError, OsPathResolverError


def home_path() -> Path:
    return Path.home()


class CacheFolderCreation:
    default_folder = "FastSync"

    def __init__(self, path_to_cache: Path | str = None):
        self._path_to_cache = path_to_cache

    @property
    def path_to_cache(self):
        path_to_cache = (
            OsCachePathResolver().resolve_path(self._path_to_cache)
            / self.default_folder
        )
        self._check_cache_folder_existence(path_to_cache)

        return path_to_cache

    def _check_cache_folder_existence(self, path_to_cache):
        if not path_to_cache.exists():
            self._create_cache_folder(path_to_cache)
        else:
            logger.info(f"Directory for cache data already exists: {path_to_cache}")

    @staticmethod
    def _create_cache_folder(path_to_cache):
        try:
            path_to_cache.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory for cache data ready: {path_to_cache}")
        except PermissionError:
            logger.error(f"Permission denied: {path_to_cache}")
            raise CacheFolderCreationError(path_to_cache)


class OsCachePathResolver:
    def resolve_path(self, path: Path | str = None) -> Path:
        if path is None:
            return self._get_default_path()
        return self._get_custom_path(path)

    @staticmethod
    def _validate_path(path: Path):
        if not path.exists():
            logger.error(f"Path not found: {path}")
            raise OsPathResolverError(filename=path)

    @staticmethod
    def _get_default_path() -> Path:
        system = platform.system().upper()
        try:
            os_type = OsCacheTypePath[system]
        except KeyError:
            logger.warning(f"Unknown OS: {system}, falling back to default style paths")
            return OsCacheTypePath.default()
        else:
            return os_type.value

    def _get_custom_path(self, path: Path | str) -> Path:
        custom_path = Path(path)
        self._validate_path(custom_path)
        return custom_path


class OsCacheTypePath(Enum):
    WINDOWS = Path(home_path(), "AppData", "Local")
    LINUX = Path(home_path(), ".cache")
    DEFAULT = home_path()

    @classmethod
    def default(cls):
        return cls.DEFAULT.value
