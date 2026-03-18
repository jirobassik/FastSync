from fast_sync.folder_reader.base import Reader

from .base import FolderDecorator, FolderRecursiveReaderComponent


class FolderFilterReader(Reader):
    def __init__(self, *args: FolderDecorator):
        self.filters = args

    def __repr__(self):
        return f"{self.__class__.__name__}(filters={self._filters!r})"

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value: tuple[FolderDecorator]):
        self._filters = sorted(value, key=lambda filter_class: filter_class.priority)

    def read(self, folder):
        folder_reader = FolderRecursiveReaderComponent(folder)
        for filter_object in self._filters:
            if filter_object.filter_values:
                folder_reader = filter_object(folder_reader)
        filtered_folder_content = folder_reader.operation()
        return filtered_folder_content
