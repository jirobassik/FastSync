class NotValidFilterInput(Exception):
    def __str__(self):
        return "Not valid filter input"


class SyncManagerError(AttributeError):
    pass


class PathSetupError(ValueError):
    pass


class ValidationPathError(ValueError):
    pass
