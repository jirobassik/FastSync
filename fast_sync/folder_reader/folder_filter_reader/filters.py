from .base import FolderDecorator, FolderReaderComponent


class FilterFolders(FolderDecorator):
    """
    Must always be specified first in arguments to FolderFilterReader.
    """

    priority = 0

    def operation(self):
        iter_dir = FolderReaderComponent(self.component.folder).operation()
        for file in iter_dir:
            if file.is_dir():
                if file.name in self.filter_values:
                    continue
                self.component.folder = file
                yield from self.operation()
                continue
            yield file


class FilterExtensionsFolder(FolderDecorator):
    priority = 1

    def operation(self):
        for file in self.component.operation():
            if file.suffix in self.filter_values:
                yield file
