import pytest

from fast_sync.hash_content_folder.hash_content_folder_caching.cache_folder_creation import (
    OsCachePathResolver,
)
from fast_sync.utils.errors import CacheFolderCreationError, OsPathResolverError

from .conftest import FIXTURE_DIR_INTERNAL


def test_default_path(cache_folder_creation):

    path_resolver = OsCachePathResolver().resolve_path()
    default_folder = cache_folder_creation().path_to_cache
    actual_folder = path_resolver / "FastSync"
    assert default_folder == actual_folder


def test_valid_custom_path(tmp_path, cache_folder_creation):
    custom_folder = cache_folder_creation(tmp_path).path_to_cache
    actual_folder = tmp_path / "FastSync"
    assert custom_folder.exists()
    assert custom_folder == actual_folder


def test_not_valid_custom_path(cache_folder_creation):
    with pytest.raises(OsPathResolverError):
        getattr(cache_folder_creation("not/valid/path"), "path_to_cache")


@pytest.mark.local
def test_permission_error_path(cache_folder_creation):
    permission_error_folder = FIXTURE_DIR_INTERNAL / "PermError/csv"
    with pytest.raises(CacheFolderCreationError):
        getattr(
            cache_folder_creation(permission_error_folder),
            "path_to_cache",
        )
