from pytest_unordered import unordered

from fast_sync.equal_resolver import EqualFinder


def test_find_equal_files(folder_structure_hash):
    expected_files = ["t2.csv", "t24.csv", "t24.csv", "t2.json", "t2.json"]
    equal_finder = EqualFinder(only_name=True)
    actual_files = equal_finder.find_equal(folder_structure_hash)
    assert unordered(expected_files) == actual_files


def test_find_equal_files_group_by_hash():
    pass


def test_equal_resolver_empty_hash():
    pass


def test_equal_resolver_empty_equal_el():
    pass


def test_equal_resolver_no_choose_file():
    pass
