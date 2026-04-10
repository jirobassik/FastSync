import pytest
from pytest_unordered import unordered, unordered_deep

from fast_sync.duplicate_resolver.duplicate_filtering import (
    FilterDuplicateByDateCreationTime,
)
from fast_sync.duplicate_resolver.duplicate_finder import (
    DuplicateFinder,
    DuplicateFinderGroupByHash,
)
from fast_sync.duplicate_resolver.duplicate_resolver import DuplicateResolver
from fast_sync.utils.errors import (
    EqualResolverError,
    FilterDublicateByDateCreationTimeError,
)

from .conftest import FIXTURE_DIR_INTERNAL


def test_equal_finder_files(folder_structure_hash):
    expected_files = ["t2.csv", "t24.csv", "t24.csv", "t2.json", "t2.json"]
    equal_finder = DuplicateFinder(only_name=True)
    actual_files = equal_finder.find_duplicate(folder_structure_hash)
    assert unordered(expected_files) == actual_files


def test_equal_finder_files_group_by_hash(folder_structure_hash):
    expected_files = [["t2.csv", "t24.csv", "t24.csv"], ["t2.json", "t2.json"]]
    equal_finder = DuplicateFinderGroupByHash(only_name=True)
    actual_files = equal_finder.find_duplicate(folder_structure_hash)
    assert unordered_deep(expected_files) == actual_files


def test_equal_resolver_empty_equal_el():
    equal_resolver = DuplicateResolver()
    equal_resolver.path_setup(FIXTURE_DIR_INTERNAL / "Simple1")
    with pytest.raises(EqualResolverError):
        equal_resolver.get_duplicate_elements()


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
        FilterDuplicateByDateCreationTime(filter_by="newesd")


def test_duplicate_resolver_container(configure_duplicate_resolver_container):
    expected_files = ["folder1/file56.txt", "folder1/config.yaml"]

    duplicate_resolver_container = configure_duplicate_resolver_container
    dublicates_files = duplicate_resolver_container._filter_duplicates.filter_duplicate(
        duplicate_resolver_container.get_duplicate_elements()
    )
    actual_files = list(
        map(
            lambda x: x.relative_to(duplicate_resolver_container.path).as_posix(),
            dublicates_files,
        )
    )
    assert unordered(actual_files) == expected_files
