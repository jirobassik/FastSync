from pathlib import Path

import pytest

from fast_sync.utils.error import PathSetupError, ValidationPathError


def test_attr_before_path_setup(path_setup):
    with pytest.raises(PathSetupError):
        getattr(path_setup, "left_folder")


def test_attr_after_path_setup(path_setup):
    path_setup.left_folder = "/home/puzer/OS_emulate/Folder1"
    assert path_setup.left_folder == Path("/home/puzer/OS_emulate/Folder1")


def test_attr_already_pathlike(path_setup):
    path_setup.left_folder = Path("/home/puzer/OS_emulate/Folder1")
    assert path_setup.left_folder == Path("/home/puzer/OS_emulate/Folder1")


def test_attr_path_not_found(path_setup):
    with pytest.raises(ValidationPathError):
        path_setup.left_folder = "/home/puzer/OS_emulate/Fol"


def test_attr_path_to_file(path_setup, internal_folders_simple):
    left_path, right_path = internal_folders_simple
    with pytest.raises(ValidationPathError):
        path_setup.left_folder = Path(left_path / "csv" / "t2.csv").as_posix()


def test_path_setup(path_setup):
    path_setup.path_setup(
        "/home/puzer/OS_emulate/Folder1",
        "/home/puzer/OS_emulate/Folder2",
    )
    assert path_setup.left_folder == Path("/home/puzer/OS_emulate/Folder1")
    assert path_setup.right_folder == Path("/home/puzer/OS_emulate/Folder2")


def test_path_setup_not_valid(path_setup):
    with pytest.raises(ValidationPathError):
        path_setup.path_setup(
            "/home/puzer/OS_emulate/Fold",
            "/home/per/OS_emulate/Folder2",
        )
