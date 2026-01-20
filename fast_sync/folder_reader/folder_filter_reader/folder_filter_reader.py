from .base import FolderRecursiveReaderComponent


class FolderFilterReader:
    def __init__(self, *args):
        self._filters = args

    def operation(self, folder):
        folder_reader = FolderRecursiveReaderComponent(folder)
        for filter_object in self._filters:
            if filter_object.filter_values:
                folder_reader = filter_object(folder_reader)
        filtered_folder_content = folder_reader.operation()
        return filtered_folder_content
