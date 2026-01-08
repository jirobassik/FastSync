from .base import FolderRecursiveReaderComponent
from .filters_manager import FilterContentManager


class FolderFilterReader(FilterContentManager):
    def __init__(self, extensions, folders):
        super().__init__(extensions, folders)

    def operation(self, folder):
        folder_reader = FolderRecursiveReaderComponent(folder)
        for filter_object in type(self).filters:
            if filter_object.filter_value is not None:
                folder_reader = filter_object(folder_reader)
        filtered_folder_content = folder_reader.operation()
        return filtered_folder_content
