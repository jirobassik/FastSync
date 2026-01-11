from typing import Callable

from fast_sync.utils.types import ListHashPathKeyValue


class DiffFolder:
    __slots__ = ("_left_hash_dict", "_right_hash_dict")

    def __init__(self, left_hash: ListHashPathKeyValue, right_hash: ListHashPathKeyValue):
        self._left_hash_dict = dict(left_hash)
        self._right_hash_dict = dict(right_hash)

    @property
    def missing_left_dict(self):
        return self._missing_dict(self._right_hash_dict, self._missing_left)

    @property
    def missing_right_dict(self):
        return self._missing_dict(self._left_hash_dict, self._missing_right)

    def _missing_left(self):
        return self._missing_files(self._right_hash_dict, self._left_hash_dict)

    def _missing_right(self):
        return self._missing_files(self._left_hash_dict, self._right_hash_dict)

    @staticmethod
    def _missing_files(first_hash_dict, second_hash_dict) -> set:
        return set(first_hash_dict.keys()) - set(second_hash_dict.keys())

    @staticmethod
    def _missing_dict(first_hash_dict, missing_set: Callable):
        return {value: first_hash_dict.get(value) for value in missing_set()}
