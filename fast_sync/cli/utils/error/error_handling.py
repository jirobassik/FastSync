from typing import Callable

from fast_sync.utils.errors import HashContentFolderError

from .errors import PermissionDeniedError


def error_handling(func: Callable):
    try:
        func()
    except HashContentFolderError as e:
        raise PermissionDeniedError(e.message, hint="Permission denied")
