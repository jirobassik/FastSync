from pathlib import Path

import pytest

from fast_sync.utils.error import PathSetupError, ValidationPathError


def test_attr_before_path_setup(path_setup):
    with pytest.raises(PathSetupError):
        getattr(path_setup, "left_folder")


def test_attr_after_path_setup(path_setup, internal_folders_simple):
    left_folder, _ = internal_folders_simple(as_posix=True)
    path_setup.left_folder = left_folder
    assert path_setup.left_folder.samefile(left_folder)


def test_attr_already_pathlike(path_setup, internal_folders_simple):
    left_folder, _ = internal_folders_simple()
    path_setup.left_folder = Path(left_folder)
    assert path_setup.left_folder.samefile(left_folder)


def test_attr_path_not_found(path_setup):
    with pytest.raises(ValidationPathError):
        path_setup.left_folder = "/home/puzer/OS_emulate/Fol"


def test_attr_path_to_file(path_setup, internal_folders_simple):
    left_path, right_path = internal_folders_simple()
    with pytest.raises(ValidationPathError):
        path_setup.left_folder = Path(left_path / "csv" / "t2.csv").as_posix()


def test_path_setup(path_setup, internal_folders_simple):
    left_folder, right_folder = internal_folders_simple(as_posix=True)
    path_setup.path_setup(
        left_folder,
        right_folder,
    )
    assert path_setup.left_folder.samefile(left_folder)
    assert path_setup.right_folder.samefile(right_folder)


def test_path_setup_not_valid(path_setup, internal_folders_simple):
    with pytest.raises(ValidationPathError):
        path_setup.path_setup(
            "/home/puzer/OS_emulate/Fold",
            "/home/per/OS_emulate/Folder2",
        )
