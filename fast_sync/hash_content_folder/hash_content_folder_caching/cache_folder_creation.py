import platform
from enum import Enum
from pathlib import Path

from loguru import logger

from fast_sync.utils.error import CacheFolderCreationError, OsPathResolverError


def home_path() -> Path:
    return Path.home()


class CacheFolderCreation:
    default_folder = "FastSync"

    def __init__(self, path_to_folder: Path | str = None):
        self._path_to_folder = OsPathResolver().resolve_path(path_to_folder)
        self._create_folder()

    @property
    def path_to_folder(self):
        return self._path_to_folder

    def _create_folder(self):
        self._path_to_folder = self._path_to_folder / self.default_folder
        if not self._path_to_folder.exists():
            try:
                self._path_to_folder.mkdir(parents=True, exist_ok=True)
                logger.info(f"Directory ready: {self._path_to_folder}")
            except PermissionError:
                logger.error(f"Permission denied: {self._path_to_folder}")
                raise CacheFolderCreationError(self._path_to_folder)


class OsPathResolver:
    def resolve_path(self, path: Path | str = None) -> Path:
        if path is None:
            pathlike = self._get_default_path()
        else:
            pathlike = self._get_custom_path(path)

        self._validate_path(pathlike)
        return pathlike

    @staticmethod
    def _validate_path(path: Path):
        if not path.exists():
            logger.error(f"Path not found: {path}")
            raise OsPathResolverError(filename=path)

    @staticmethod
    def _get_default_path() -> Path:
        system = platform.system().upper()
        try:
            os_type = OsTypePath[system]
        except KeyError:
            logger.warning(f"Unknown OS: {system}, falling back to default style paths")
            return OsTypePath.default()
        else:
            return os_type.value

    @staticmethod
    def _get_custom_path(path: Path | str) -> Path:
        custom_path = Path(path)
        return custom_path


class OsTypePath(Enum):
    WINDOWS = Path(home_path(), "AppData", "Local")
    LINUX = Path(home_path(), ".cache")
    DEFAULT = home_path()

    @classmethod
    def default(cls):
        return cls.DEFAULT.value
