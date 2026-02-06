import pytest

from fast_sync import FolderReader, SyncManager
from fast_sync.utils.error import ValidationPathError


def test_continue_execute_with_not_valid_path(internal_folders_simple):
    _, right_folder = internal_folders_simple(as_posix=True)
    reader = FolderReader()
    sync_manager = SyncManager(reader)
    with pytest.raises(ValidationPathError):
        sync_manager.path_setup("/home/puzer/OS_emulate/Fo", right_folder)
        sync_manager.analyze()
