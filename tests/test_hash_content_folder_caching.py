from pathlib import Path

from fast_sync import HashContentFolderCaching
from fast_sync.utils.constant import APP_NAME


def test_creation_cache_file(tmp_path, cache_folder_creation):
    expected_path = tmp_path / APP_NAME / "cache.db"
    actual_path = Path(
        HashContentFolderCaching(
            cache_path=cache_folder_creation(tmp_path)
        )._cache.directory,
        "cache.db",
    )
    assert actual_path.exists()
    assert expected_path == actual_path
