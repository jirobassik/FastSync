from typing import Callable

from fast_sync.cli.utils.error_output import PermissionDeniedError
from fast_sync.utils.error import HashCalculationError


def permission_denied_handling(func: Callable):
    try:
        func()
    except HashCalculationError as e:
        raise PermissionDeniedError(e.filename, hint="Permission denied")
