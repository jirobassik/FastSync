import pytest
from fixtures import *  # noqa: F403

from fast_sync.folder_reader import FolderReader
from fast_sync.main import FastSync


@pytest.fixture(scope="session")
def fast_sync_simple_folder_default_reader(
    create_base_folder,
    simple_folder_structure1,
    simple_folder_structure2,
    fill_folder_content,
):
    left_folder = fill_folder_content(
        create_base_folder("base_folder1"), simple_folder_structure1
    )
    right_folder = fill_folder_content(
        create_base_folder("base_folder2"), simple_folder_structure2
    )

    reader = FolderReader()
    fast_sync = FastSync(left_folder, right_folder, reader)
    fast_sync.analyze()
    return fast_sync



@pytest.fixture(scope="session")
def fast_sync_nested_simple_folder_default_reader(
    create_base_folder,
    nested_simple_folder_structure1,
    simple_folder_structure2,
    fill_folder_content,
):
    left_folder = fill_folder_content(
        create_base_folder("base_folder1"), nested_simple_folder_structure1
    )
    right_folder = fill_folder_content(
        create_base_folder("base_folder2"), simple_folder_structure2
    )

    reader = FolderReader()
    fast_sync = FastSync(left_folder, right_folder, reader)
    fast_sync.analyze()
    return fast_sync

