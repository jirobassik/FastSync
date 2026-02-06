import pytest

from fast_sync import FolderReader, SyncManager
from fast_sync.utils.error import ValidationPathError


def test_continue_execute_with_not_valid_path():
    reader = FolderReader()
    sync_manager = SyncManager(reader)
    with pytest.raises(ValidationPathError):
        sync_manager.path_setup(
            "/home/puzer/OS_emulate/Fo",
            "/home/puzer/OS_emulate/Folder2",
        )
        sync_manager.analyze()
