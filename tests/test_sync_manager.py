import pytest

from fast_sync import FolderReader, SyncManager
from fast_sync.utils.error import HashCalculationError, ValidationPathError


def test_continue_execute_with_not_valid_path(internal_folders_simple):
    _, right_folder = internal_folders_simple(as_posix=True)
    reader = FolderReader()
    sync_manager = SyncManager(reader)
    with pytest.raises(ValidationPathError):
        sync_manager.path_setup("/home/puzer/OS_emulate/Fo", right_folder)
        sync_manager.analyze()

@pytest.mark.local
def test_hash_calculation_error(internal_folders_simple):
    left_folder, right_folder = internal_folders_simple(left_f="PermError")
    reader = FolderReader()
    sync_manager = SyncManager(reader)
    with pytest.raises(HashCalculationError):
        sync_manager.path_setup(left_folder, right_folder)
        sync_manager.analyze()
