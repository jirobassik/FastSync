from typing import Callable

from fast_sync.utils.errors import HashCalculationError

from .errors import PermissionDeniedError


def error_handling(func: Callable):
    try:
        func()
    except HashCalculationError as e:
        raise PermissionDeniedError(e.filename, hint="Permission denied")
