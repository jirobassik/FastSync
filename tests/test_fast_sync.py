from pathlib import Path

import pytest
from pytest_unordered import unordered


@pytest.mark.little
def test_diff_empty_left_folder(fast_sync_simple_folder_default_reader_left_empty):
    """Check missing files in left folder (empty), right folder with simple structure folders"""
    expected_files = ["file2.txt", "users.csv", "file1.txt"]
    actual_files = [
        file.name
        for file in fast_sync_simple_folder_default_reader_left_empty.left_missing_files()
    ]
    assert unordered(actual_files) == expected_files


@pytest.mark.little
def test_diff_empty_right_folder(fast_sync_simple_folder_default_reader_right_empty):
    """Check missing files in right folder (empty), left folder with simple structure folders"""
    expected_files = ["data.json", "config.yaml", "data.json", "file1.txt"]
    actual_files = [
        file.name
        for file in fast_sync_simple_folder_default_reader_right_empty.right_missing_files()
    ]
    assert unordered(actual_files) == expected_files


@pytest.mark.little
def test_diff_empty_left_folder_all_empty(
    fast_sync_simple_folder_default_reader_all_empty,
):
    """Check missing files in left folder, all folders empty"""
    expected_files = []
    actual_files = list(
        fast_sync_simple_folder_default_reader_all_empty.left_missing_files()
    )
    assert actual_files == expected_files


@pytest.mark.little
def test_diff_empty_right_folder_all_empty(
    fast_sync_simple_folder_default_reader_all_empty,
):
    """Check missing files in right folder, all folders empty"""
    expected_files = []
    actual_files = list(
        fast_sync_simple_folder_default_reader_all_empty.right_missing_files()
    )
    assert actual_files == expected_files


@pytest.mark.little
def test_diff_left_folder(fast_sync_simple_folder_default_reader):
    """Check missing files in left folder with simple structure folders"""
    expected_files = ["file2.txt", "users.csv"]
    actual_files = [
        file.name
        for file in fast_sync_simple_folder_default_reader.left_missing_files()
    ]
    assert unordered(actual_files) == expected_files


@pytest.mark.little
def test_diff_right_folder(fast_sync_simple_folder_default_reader):
    """Check missing files in right folder with simple structure folders"""
    expected_files = ["data.json", "config.yaml", "data.json"]
    actual_files = [
        file.name
        for file in fast_sync_simple_folder_default_reader.right_missing_files()
    ]
    assert unordered(actual_files) == expected_files


@pytest.mark.little
def test_diff_left_folder_nested(
    fast_sync_left_nested_simple_folder_default_reader,
):
    """Check missing files in left folder with nested structure"""
    expected_files = ["file1.txt", "file2.txt", "users.csv"]
    actual_files = [
        file.name
        for file in fast_sync_left_nested_simple_folder_default_reader.left_missing_files()
    ]
    assert unordered(actual_files) == expected_files


@pytest.mark.little
def test_diff_right_folder_nested(
    fast_sync_left_nested_simple_folder_default_reader,
):
    """Check missing files in right folder with nested structure"""
    expected_files = [
        "config.yaml",
        "file1.txt",
        "data.json",
        "config.yaml",
        "data.json",
    ]
    actual_files = [
        file.name
        for file in fast_sync_left_nested_simple_folder_default_reader.right_missing_files()
    ]
    assert unordered(actual_files) == expected_files


@pytest.mark.little
def test_diff_all_folder_nested(
    fast_sync_all_nested_simple_folder_default_reader,
):
    """Check missing files in left folder, left and right folder with nested structure"""
    expected_files = ["file2.txt", "users.csv"]
    actual_files = [
        file.name
        for file in fast_sync_all_nested_simple_folder_default_reader.left_missing_files()
    ]
    assert unordered(actual_files) == expected_files


FIXTURE_DIR = Path().home() / "OS_emulate"


@pytest.mark.slow
@pytest.mark.big
@pytest.mark.datafiles(
    FIXTURE_DIR / "pytest Small music1",
    FIXTURE_DIR / "pytest Small music2",
    on_duplicate="ignore",
    keep_top_dir=True,
)
def test_diff_left_big_folder(default_fast_sync_fabric, datafiles):
    """Check missing files in left folder, big left and right folders from local storage"""
    expected_files = [
        "AlbumArt_{B5020207-474E-4720-96D5-B12E861D6A00}_Large.jpg",
        "AlbumArt_{99332582-9CB8-42B0-BB5E-F2A75F45E3F3}_Small.jpg",
        "AlbumArt_{87A4D4FA-261C-44D5-943E-F29175DF743C}_Small.jpg",
        "AlbumArt_{00000000-0000-0000-0000-000000000000}_Small.jpg",
        "AlbumArt_{1270E3A6-FBC2-4550-8C51-A80459180550}_Small.jpg",
        "Receptor - Russkly Specnaz.mp3",
        "Rusty K - Juggernaut (Cut).mp3",
        "Drummatix - К Пропасти.mp3",
        "TAMFREE100_40_Zerx_LockpicK_-_Difficult_Point.wav",
    ]
    left_folder = datafiles / "pytest Small music1"
    right_folder = datafiles / "pytest Small music2"
    fast_sync = default_fast_sync_fabric(
        left_folder.as_posix(), right_folder.as_posix()
    )
    actual_files = [file.name for file in fast_sync.left_missing_files()]
    assert unordered(actual_files) == expected_files


@pytest.mark.slow
@pytest.mark.big
@pytest.mark.datafiles(
    FIXTURE_DIR / "pytest Small music1",
    FIXTURE_DIR / "pytest Small music2",
    on_duplicate="ignore",
    keep_top_dir=True,
)
def test_diff_right_big_folder(default_fast_sync_fabric, datafiles):
    """Check missing files in right folder, big left and right folders from local storage"""
    expected_files = [
        "Lost Weekend Western Swing Band - Let's Ride Into The Sunset Together.mp3",
        "Tommy Smith ft. Darell Wayne Perry - Goin Under.mp3",
        "Bert Weedon - Happy Times.mp3",
        "Helen Forrest - Mad About the Boy.mp3",
        "Underside_5_mixed_by_Bes.mp3",
        "Mix_tracklist.txt",
        "Underside_5_LP.pdf",
    ]
    left_folder = datafiles / "pytest Small music1"
    right_folder = datafiles / "pytest Small music2"
    fast_sync = default_fast_sync_fabric(
        left_folder.as_posix(), right_folder.as_posix()
    )
    actual_files = [file.name for file in fast_sync.right_missing_files()]
    assert unordered(actual_files) == expected_files


@pytest.mark.filters
@pytest.mark.slow
@pytest.mark.big
@pytest.mark.datafiles(
    FIXTURE_DIR / "pytest Small music1",
    FIXTURE_DIR / "pytest Small music2",
    on_duplicate="ignore",
    keep_top_dir=True,
)
def test_diff_left_big_folder_with_filters(filter_reader_fast_sync_fabric, datafiles):
    """Check missing files in left folder, big left and right folders from local storage, extensions filters"""
    expected_files = [
        "AlbumArt_{B5020207-474E-4720-96D5-B12E861D6A00}_Large.jpg",
        "AlbumArt_{99332582-9CB8-42B0-BB5E-F2A75F45E3F3}_Small.jpg",
        "AlbumArt_{87A4D4FA-261C-44D5-943E-F29175DF743C}_Small.jpg",
        "AlbumArt_{00000000-0000-0000-0000-000000000000}_Small.jpg",
        "AlbumArt_{1270E3A6-FBC2-4550-8C51-A80459180550}_Small.jpg",
        "TAMFREE100_40_Zerx_LockpicK_-_Difficult_Point.wav",
    ]
    left_folder = datafiles / "pytest Small music1"
    right_folder = datafiles / "pytest Small music2"
    fast_sync = filter_reader_fast_sync_fabric(
        left_folder.as_posix(),
        right_folder.as_posix(),
        extensions=(
            ".jpg",
            ".wav",
        ),
        folders=(),
    )
    actual_files = [file.name for file in fast_sync.left_missing_files()]
    assert unordered(actual_files) == expected_files


@pytest.mark.filters
@pytest.mark.slow
@pytest.mark.big
@pytest.mark.datafiles(
    FIXTURE_DIR / "pytest Small music1",
    FIXTURE_DIR / "pytest Small music2",
    on_duplicate="ignore",
    keep_top_dir=True,
)
def test_diff_right_big_folder_with_filters(filter_reader_fast_sync_fabric, datafiles):
    """Check missing files in right folder, big left and right folders from local storage, extensions filters"""
    expected_files = [
        "Mix_tracklist.txt",
    ]
    left_folder = datafiles / "pytest Small music1"
    right_folder = datafiles / "pytest Small music2"
    fast_sync = filter_reader_fast_sync_fabric(
        left_folder.as_posix(),
        right_folder.as_posix(),
        extensions=(".txt",),
        folders=(),
    )
    actual_files = [file.name for file in fast_sync.right_missing_files()]
    assert unordered(actual_files) == expected_files


@pytest.mark.filters
@pytest.mark.slow
@pytest.mark.big
@pytest.mark.parametrize(
    "extensions,folders,expected_files",
    [
        (
            (),
            ("Underside 5 LP Limited box edition", "Rus dnb"),
            [
                "AlbumArt_{B5020207-474E-4720-96D5-B12E861D6A00}_Large.jpg",
                "AlbumArt_{99332582-9CB8-42B0-BB5E-F2A75F45E3F3}_Small.jpg",
                "AlbumArt_{87A4D4FA-261C-44D5-943E-F29175DF743C}_Small.jpg",
                "AlbumArt_{00000000-0000-0000-0000-000000000000}_Small.jpg",
                "AlbumArt_{1270E3A6-FBC2-4550-8C51-A80459180550}_Small.jpg",
            ],
        ),
        (
            (".jpg", ".wav"),
            ("Rus dnb",),
            [
                "AlbumArt_{B5020207-474E-4720-96D5-B12E861D6A00}_Large.jpg",
                "AlbumArt_{99332582-9CB8-42B0-BB5E-F2A75F45E3F3}_Small.jpg",
                "AlbumArt_{87A4D4FA-261C-44D5-943E-F29175DF743C}_Small.jpg",
                "AlbumArt_{00000000-0000-0000-0000-000000000000}_Small.jpg",
                "AlbumArt_{1270E3A6-FBC2-4550-8C51-A80459180550}_Small.jpg",
                "TAMFREE100_40_Zerx_LockpicK_-_Difficult_Point.wav",
            ],
        ),
        (
            (".mp3", ".wav"),
            ("wav",),
            [
                "Receptor - Russkly Specnaz.mp3",
                "Rusty K - Juggernaut (Cut).mp3",
                "Drummatix - К Пропасти.mp3",
            ],
        ),
    ],
)
@pytest.mark.datafiles(
    FIXTURE_DIR / "pytest Small music1",
    FIXTURE_DIR / "pytest Small music2",
    on_duplicate="ignore",
    keep_top_dir=True,
)
def test_diff_left_big_folder_with_various_filters(
    filter_reader_fast_sync_fabric, datafiles, extensions, folders, expected_files
):
    """Check missing files in left folder, big left and right folders from local storage, extensions and folders filters"""
    left_folder = datafiles / "pytest Small music1"
    right_folder = datafiles / "pytest Small music2"
    fast_sync = filter_reader_fast_sync_fabric(
        left_folder.as_posix(),
        right_folder.as_posix(),
        extensions=extensions,
        folders=folders,
    )
    actual_files = [file.name for file in fast_sync.left_missing_files()]
    assert unordered(actual_files) == expected_files
