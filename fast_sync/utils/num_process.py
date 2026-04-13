from typing import Optional

import psutil


def number_of_usable_cpus() -> int:
    return len(psutil.Process().cpu_affinity())


class NumProcess:
    def __init__(
        self,
        min_num_processes: int = 1,
        max_num_processes: Optional[int] = None,
    ):
        self.min_num_processes = min_num_processes
        if max_num_processes is None:
            max_num_processes = number_of_usable_cpus()
        self.max_num_processes = max_num_processes

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.private_name, value)

    def validate(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Expected {value!r} to be an int")
        if not self.min_num_processes <= value <= self.max_num_processes:
            raise ValueError(
                f"Not valid num processes value. "
                f"Valid range: {self.min_num_processes}<=x<={self.max_num_processes} "
            )
