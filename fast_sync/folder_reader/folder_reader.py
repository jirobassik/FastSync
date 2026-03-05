from pathlib import Path

from .folder_filter_reader import FolderRecursiveReaderComponent


class FolderReader:
    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def operation(folder: Path):
        return FolderRecursiveReaderComponent(folder).operation()
