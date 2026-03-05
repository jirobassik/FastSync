class NotValidFilterInput(Exception):
    def __str__(self):
        return "Not valid filter input"


class HashContentFolderError(Exception):
    def __init__(self, message, err_name="Undefined error", error_class=None):
        self.message = message
        self.err_name = err_name
        self.error_class = error_class

    def __str__(self):
        return f"{self.message}: {self.err_name}"


class CacheFolderCreationError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"Cannot create directory at {self.filename}: Permission denied"


class OsPathResolverError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"Path not found: {self.filename}"


class PathSetupError(ValueError):
    pass


class ValidationPathError(ValueError):
    pass


class SyncManagerError(AttributeError):
    pass
