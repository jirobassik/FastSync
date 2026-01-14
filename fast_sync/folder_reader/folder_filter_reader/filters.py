from .base import FolderDecorator, FolderReaderComponent


class FilterFolders(FolderDecorator):
    filter_name = 'folders'

    def operation(self):
        iter_dir = FolderReaderComponent(self.component.folder).operation()
        for file in iter_dir:
            if file.is_dir():
                if file.name in type(self).filter_value:
                    continue
                self.component.folder = file
                yield from self.operation()
                continue
            yield file



class FilterExtensionsFolder(FolderDecorator):
    filter_name = 'extensions'

    def operation(self):
        for file in self.component.operation():
            if file.suffix in type(self).filter_value:
                yield file
