from pathlib import Path

from loguru import logger

from fast_sync.utils.errors import PathSetupError, ValidationPathError


class ValidPath:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner) -> Path:
        if (setuped_path := instance.__dict__.get(self._name)) is None:
            raise PathSetupError("Path not setup. Use `.setup_paths`")
        return setuped_path

    def __set__(self, instance, value: str | Path):
        set_path = Path(value)
        self.validate(set_path)
        instance.__dict__[self._name] = set_path

    @staticmethod
    def validate(value: Path):
        if not value.exists():
            error_message = f"Path does not exist: '{value}'"
            logger.error(error_message)
            raise ValidationPathError(error_message)
        if not value.is_dir():
            error_message = f"Path must be dir, not file: '{value.suffix}'"
            logger.error(error_message)
            raise ValidationPathError(error_message)


class PathSetup:
    left_folder: Path = ValidPath()
    right_folder: Path = ValidPath()

    def path_setup(self, left_path: str | Path, right_path: str | Path):
        self.left_folder = left_path
        self.right_folder = right_path
