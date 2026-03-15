import abc
from pathlib import Path


class Reader(abc.ABC):
    @abc.abstractmethod
    def read(self, folder: Path):
        pass
