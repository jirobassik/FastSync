class NotValidFilterInput(Exception):
    def __str__(self):
        return "Not valid filter input"


class SyncManagerError(AttributeError):
    pass
