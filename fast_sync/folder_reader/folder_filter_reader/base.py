from abc import ABC, abstractmethod
from pathlib import Path


class Component(ABC):

    @abstractmethod
    def operation(self):
        pass


class ReaderComponent(Component, ABC):
    def __init__(self, folder: Path):
        self.folder = folder


class FolderReaderComponent(ReaderComponent):

    def operation(self):
        return self.folder.iterdir()


class FolderRecursiveReaderComponent(ReaderComponent):

    def operation(self):
        return (file for file in self.folder.rglob(pattern="*") if not file.is_dir())


class FilterValues:
    def __init__(self, *args):
        self.filter_values = args

    @property
    def filter_values(self):
        return self._filter_values

    @filter_values.setter
    def filter_values(self, value):
        self._filter_values = self.filter_value_checker(value)

    @staticmethod
    def filter_value_checker(value):
        return value


class FolderDecorator(FilterValues, Component):
    _component: Component = None

    def __init__(self, *args) -> None:
        super().__init__(*args)

    def __call__(self, component: Component):
        self._component = component
        return self

    @property
    def component(self) -> Component:
        return self._component

    def operation(self):
        return self._component.operation()
