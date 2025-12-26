from .base import FolderDecorator, FolderReaderComponent


class FilterFolders(FolderDecorator):
    filter_value = None

    def operation(self):
        iter_dir = FolderReaderComponent(self.component.folder).operation()
        for file in iter_dir:
            if file.name in type(self).filter_value:
                continue
            yield file
            if file.is_dir():
                self.component.folder = file
                yield from self.operation()


class FilterExtensionsFolder(FolderDecorator):
    filter_value = None

    def operation(self):
        for file in self.component.operation():
            if file.suffix in type(self).filter_value:
                yield file
