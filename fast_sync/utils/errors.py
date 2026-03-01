class NotValidFilterInput(Exception):
    def __str__(self):
        return "Not valid filter input"


class HashCalculationError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"Cannot calculate hash at {self.filename}: Permission denied"


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
