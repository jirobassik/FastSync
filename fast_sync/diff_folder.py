from typing import Callable


class HashComparator:
    pass


class DiffFolder:
    def __init__(self, left_hash, right_hash):
        self.left_hash_dict = dict(left_hash)
        self.right_hash_dict = dict(right_hash)

    @property
    def missing_left_dict(self):
        return self.missing_dict(self.right_hash_dict, self.__missing_left)

    @property
    def missing_right_dict(self):
        return self.missing_dict(self.left_hash_dict, self.__missing_right)

    def __missing_left(self):
        return self.missing_files(self.right_hash_dict, self.left_hash_dict)

    def __missing_right(self):
        return self.missing_files(self.left_hash_dict, self.right_hash_dict)

    @staticmethod
    def missing_files(first_hash_dict, second_hash_dict) -> set:
        return set(first_hash_dict.keys()) - set(second_hash_dict.keys())

    @staticmethod
    def missing_dict(first_hash_dict, missing_set: Callable):
        return {value: first_hash_dict.get(value) for value in missing_set()}
