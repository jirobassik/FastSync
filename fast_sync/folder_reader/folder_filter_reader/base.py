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


class FolderDecorator(Component):
    _component: Component = None
    filter_value = None
    filter_name = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self):
        return self._component.operation()
