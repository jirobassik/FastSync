import pytest
from pytest_unordered import unordered, unordered_deep

from fast_sync.duplicate_resolver.duplicate_filtering import (
    FilterDublicateByDateCreationTime,
)
from fast_sync.duplicate_resolver.duplicate_finder import (
    EqualFinder,
    EqualFinderGroupByHash,
)
from fast_sync.duplicate_resolver.duplicate_resolver import EqualResolver
from fast_sync.utils.errors import (
    EqualResolverError,
    FilterDublicateByDateCreationTimeError,
)

from .conftest import FIXTURE_DIR_INTERNAL


def test_equal_finder_files(folder_structure_hash):
    expected_files = ["t2.csv", "t24.csv", "t24.csv", "t2.json", "t2.json"]
    equal_finder = EqualFinder(only_name=True)
    actual_files = equal_finder.find_equal(folder_structure_hash)
    assert unordered(expected_files) == actual_files


def test_equal_finder_files_group_by_hash(folder_structure_hash):
    expected_files = [["t2.csv", "t24.csv", "t24.csv"], ["t2.json", "t2.json"]]
    equal_finder = EqualFinderGroupByHash(only_name=True)
    actual_files = equal_finder.find_equal(folder_structure_hash)
    assert unordered_deep(expected_files) == actual_files


def test_equal_resolver_empty_equal_el():
    equal_resolver = EqualResolver()
    equal_resolver.path_setup(FIXTURE_DIR_INTERNAL / "Simple1")
    with pytest.raises(EqualResolverError):
        equal_resolver.get_equal_elements()


def test_get_newest_duplicates_files(configure_dublicate_finder_by_date):
    expected_files = ["folder1/file56.txt", "folder1/config.yaml"]
    actual_files = configure_dublicate_finder_by_date(filter_by="newest")
    assert unordered(actual_files) == expected_files


def test_get_oldest_duplicates_files(configure_dublicate_finder_by_date):
    expected_files = ["folder2/file56.txt", "folder2/config.yaml2"]
    actual_files = configure_dublicate_finder_by_date(filter_by="oldest")
    assert unordered(actual_files) == expected_files


def test_not_valid_filter_by_value():
    with pytest.raises(FilterDublicateByDateCreationTimeError):
        FilterDublicateByDateCreationTime(filter_by="newesd")
