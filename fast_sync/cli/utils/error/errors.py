from gettext import gettext as _

from click import FileError


class ConfigFileCreationError(Exception):
    def __init__(self, message, filename):
        self.message = message
        self.filename = filename

    def __str__(self):
        return f"{self.message} in {self.filename}"

    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message!r}, filename={self.filename!r})"


class OutputFormaterError(Exception):
    pass


class PermissionDeniedError(FileError):
    def format_message(self) -> str:
        return _("Could not open path {filename!r}: {message}").format(
            filename=self.ui_filename, message=self.message
        )
