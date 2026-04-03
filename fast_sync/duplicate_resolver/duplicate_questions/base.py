import abc
from pathlib import Path
from typing import ValuesView

from inquirer.themes import Theme


class BaseDublicates(abc.ABC):
    __slots__ = ["duplicates"]

    def __init__(self, duplicates: ValuesView[list[Path]]):
        self.duplicates = duplicates

    @abc.abstractmethod
    def get_duplicates(self):
        pass


class BaseQuestion(BaseDublicates):
    __slots__ = ["theme"]

    def __init__(
        self,
        duplicates: ValuesView[list[Path]],
        theme: Theme,
    ):
        super().__init__(duplicates)
        self.theme = theme

    @abc.abstractmethod
    def answer(self):
        pass

    @abc.abstractmethod
    def question(self):
        raise NotImplementedError
