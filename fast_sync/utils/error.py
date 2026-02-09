class NotValidFilterInput(Exception):
    def __str__(self):
        return "Not valid filter input"


class HashCalculationError(Exception):
    def __init__(self, filename):
        self.filename = filename


class SyncManagerError(AttributeError):
    pass


class PathSetupError(ValueError):
    pass


class ValidationPathError(ValueError):
    pass
