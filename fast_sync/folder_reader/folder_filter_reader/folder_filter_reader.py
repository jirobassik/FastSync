from .base import FolderDecorator, FolderRecursiveReaderComponent


class FolderFilterReader:
    def __init__(self, *args: FolderDecorator):
        self.filters = args

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value: tuple[FolderDecorator]):
        self._filters = sorted(value, key=lambda filter_class: filter_class.priority)

    def operation(self, folder):
        folder_reader = FolderRecursiveReaderComponent(folder)
        for filter_object in self._filters:
            if filter_object.filter_values:
                folder_reader = filter_object(folder_reader)
        filtered_folder_content = folder_reader.operation()
        return filtered_folder_content
