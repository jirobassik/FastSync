import pytest

from fast_sync.utils.path_setup import PathSetup


@pytest.fixture(scope="session")
def path_setup():
    return PathSetup()
