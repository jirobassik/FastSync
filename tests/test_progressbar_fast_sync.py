from pytest_unordered import unordered

from fast_sync.utils.progressbar import ProgressBarFastSync

from .conftest import FIXTURE_DIR_INTERNAL


def test_equal_progressbar_result_fastsync(default_fast_sync_fabric):
    folder = (FIXTURE_DIR_INTERNAL / "Simple1").as_posix()

    fast_sync_default = default_fast_sync_fabric(folder, folder)
    fast_sync_default_files = [
        file.name for file in fast_sync_default.right_missing_files()
    ]

    fast_sync_progressbar = default_fast_sync_fabric(
        folder,
        folder,
        fast_sync_method=ProgressBarFastSync,
    )
    fast_sync_progressbar_files = [
        file.name for file in fast_sync_progressbar.right_missing_files()
    ]

    assert unordered(fast_sync_default_files) == fast_sync_progressbar_files
