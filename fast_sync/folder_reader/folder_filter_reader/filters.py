from .base import FolderDecorator, FolderReaderComponent


class FilterFolders(FolderDecorator):
    """
    Всегда должен указываться первым в аргументах для FolderFilterReader
    """

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

    def operation(self):
        for file in self.component.operation():
            if file.suffix in self.filter_values:
                yield file
