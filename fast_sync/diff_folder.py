from typing import Callable

from fast_sync.utils.types import ListHashPathKeyValue


class DiffFolder:
    __slots__ = ("_left_hash_mapping", "_right_hash_mapping")

    def __init__(
        self,
        left_hash: ListHashPathKeyValue,
        right_hash: ListHashPathKeyValue,
    ):
        self._left_hash_mapping = dict(left_hash)
        self._right_hash_mapping = dict(right_hash)

    @property
    def missing_files_in_left_folder(self):
        return self._matching_missing_file_with_path(
            self._right_hash_mapping,
            self._find_missing_files_in_left_folder,
        )

    @property
    def missing_files_in_right_folder(self):
        return self._matching_missing_file_with_path(
            self._left_hash_mapping,
            self._find_missing_files_in_right_folder,
        )

    def _find_missing_files_in_left_folder(self):
        return self._find_missing_files(
            self._right_hash_mapping,
            self._left_hash_mapping,
        )

    def _find_missing_files_in_right_folder(self):
        return self._find_missing_files(
            self._left_hash_mapping,
            self._right_hash_mapping,
        )

    @staticmethod
    def _find_missing_files(first_hash_dict, second_hash_dict) -> set:
        return set(first_hash_dict.keys()) - set(second_hash_dict.keys())

    @staticmethod
    def _matching_missing_file_with_path(
        hash_mapping_from_which_missing_values_taken,
        missing_files: Callable,
    ):
        return {
            value: hash_mapping_from_which_missing_values_taken.get(value)
            for value in missing_files()
        }
