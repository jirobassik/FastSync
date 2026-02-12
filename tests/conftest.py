from pathlib import Path

import pytest

from fast_sync import FolderFilterReader
from fast_sync.folder_reader import FolderReader
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)
from fast_sync.main import FastSync
from tests.fixtures import *  # noqa: F403

FIXTURE_DIR_INTERNAL = Path(__file__).parent / "fixtures/test_folders"
FIXTURE_DIR_EXTERNAL = Path().home() / "OS_emulate"


@pytest.fixture(scope="session")
def default_fast_sync_fabric():
    def _default_fast_sync_fabric(left_folder, right_folder):
        reader = FolderReader()
        fast_sync = FastSync(reader)
        fast_sync.path_setup(left_folder, right_folder)
        fast_sync.analyze()
        return fast_sync

    return _default_fast_sync_fabric


@pytest.fixture(scope="session")
def filter_reader_fast_sync_fabric():
    def _filter_reader_fast_sync_fabric(
        left_folder,
        right_folder,
        folders: tuple,
        extensions: tuple,
    ):
        reader = FolderFilterReader(
            FilterFolders(*folders),
            FilterExtensionsFolder(*extensions),
        )
        fast_sync = FastSync(reader)
        fast_sync.path_setup(left_folder, right_folder)
        fast_sync.analyze()
        return fast_sync

    return _filter_reader_fast_sync_fabric


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader_left_empty(
    default_fast_sync_fabric,
    create_base_folder,
    right_folder_simple,
):
    return default_fast_sync_fabric(
        create_base_folder("left_folder"), right_folder_simple
    )


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader_right_empty(
    default_fast_sync_fabric,
    left_folder_simple,
    create_base_folder,
):
    return default_fast_sync_fabric(
        left_folder_simple, create_base_folder("right_folder")
    )


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader_all_empty(
    default_fast_sync_fabric,
    create_base_folder,
):
    return default_fast_sync_fabric(
        create_base_folder("left_folder"), create_base_folder("right_folder")
    )


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader(
    default_fast_sync_fabric,
    left_folder_simple,
    right_folder_simple,
):
    return default_fast_sync_fabric(left_folder_simple, right_folder_simple)


@pytest.fixture(scope="session")
def fast_sync_left_nested_simple_folder_default_reader(
    default_fast_sync_fabric,
    left_folder_nested_simple,
    right_folder_simple,
):
    return default_fast_sync_fabric(left_folder_nested_simple, right_folder_simple)


@pytest.fixture(scope="session")
def fast_sync_all_nested_simple_folder_default_reader(
    default_fast_sync_fabric,
    left_folder_nested_simple,
    right_folder_nested_simple,
):
    return default_fast_sync_fabric(
        left_folder_nested_simple, right_folder_nested_simple
    )


@pytest.fixture(scope="session")
def internal_folders_simple():
    def _internal_folders_simple(
        as_posix=False,
        left_f="Simple1",
        right_f="Simple2",
    ):
        left_folder = FIXTURE_DIR_INTERNAL / left_f
        right_folder = FIXTURE_DIR_INTERNAL / right_f
        return (
            (left_folder.as_posix(), right_folder.as_posix())
            if as_posix
            else (left_folder, right_folder)
        )

    return _internal_folders_simple
