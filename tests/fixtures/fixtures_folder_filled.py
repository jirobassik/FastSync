import pytest


@pytest.fixture(scope="session")
def left_folder_simple(
    filled_folder_factory,
    left_folder_simple_structure,
):
    return filled_folder_factory("left_folder", left_folder_simple_structure)


@pytest.fixture(scope="session")
def left_folder_nested_simple(
    filled_folder_factory,
    left_folder_nested_simple_structure,
):
    return filled_folder_factory("left_folder", left_folder_nested_simple_structure)


@pytest.fixture(scope="session")
def right_folder_simple(
    filled_folder_factory,
    right_folder_simple_structure,
):
    return filled_folder_factory("right_folder", right_folder_simple_structure)


@pytest.fixture(scope="session")
def right_folder_nested_simple(
    filled_folder_factory,
    right_folder_nested_simple_structure,
):
    return filled_folder_factory("right_folder", right_folder_nested_simple_structure)


@pytest.fixture(scope="session")
def folder_equal_data(
    filled_folder_factory,
    folders_with_equal_files_not_same_name,
):
    return filled_folder_factory("equal_folder", folders_with_equal_files_not_same_name)
