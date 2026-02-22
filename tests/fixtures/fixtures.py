import pytest

from fast_sync.hash_content_folder.hash_content_folder_caching.cache_folder_creation import (
    CacheFolderCreation,
)
from fast_sync.utils.path_setup import PathSetup


@pytest.fixture(scope="session")
def path_setup():
    return PathSetup()


@pytest.fixture(scope="session")
def cache_folder_creation():
    def _cache_folder_creation(custom_path=None):
        return CacheFolderCreation(custom_path)

    return _cache_folder_creation
