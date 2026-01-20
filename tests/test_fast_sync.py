from pytest_unordered import unordered


def test_fast_sync_diff_left_folder(fast_sync_simple_folder_default_reader):
    expected_files = ["file2.txt", "users.csv"]
    actual_files = [
        file.name
        for file in fast_sync_simple_folder_default_reader.left_missing_files()
    ]
    assert unordered(actual_files) == expected_files


def test_fast_sync_diff_right_folder(fast_sync_simple_folder_default_reader):
    expected_files = ["data.json", "config.yaml", "data.json"]
    actual_files = [
        file.name
        for file in fast_sync_simple_folder_default_reader.right_missing_files()
    ]
    assert unordered(actual_files) == expected_files


def test_fast_sync_diff_left_folder_nested(
    fast_sync_nested_simple_folder_default_reader,
):
    expected_files = ["file1.txt", "file2.txt", "users.csv"]
    actual_files = [
        file.name
        for file in fast_sync_nested_simple_folder_default_reader.left_missing_files()
    ]
    assert unordered(actual_files) == expected_files


def test_fast_sync_diff_right_folder_nested(
    fast_sync_nested_simple_folder_default_reader,
):
    expected_files = ["config.yaml", "file1.txt", "data.json", "config.yaml", "data.json"]
    actual_files = [
        file.name
        for file in fast_sync_nested_simple_folder_default_reader.right_missing_files()
    ]
    assert unordered(actual_files) == expected_files
