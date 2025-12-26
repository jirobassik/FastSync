from abc import ABC, abstractmethod
from pathlib import Path


class Component(ABC):

    @abstractmethod
    def operation(self):
        pass


class FolderReaderComponent(Component):
    def __init__(self, folder: Path):
        self.folder = folder

    def operation(self):
        return self.folder.iterdir()


class FolderRecursiveReaderComponent(Component):
    def __init__(self, folder: Path):
        self.folder = folder

    def operation(self):
        return (file for file in self.folder.rglob(pattern="*") if not file.is_dir())


class FolderDecorator(Component):
    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self):
        return self._component.operation()
