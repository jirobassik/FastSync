from pathlib import Path

from .folder_filter_reader import FolderRecursiveReaderComponent


class FolderReader:

    @staticmethod
    def operation(folder: Path):
        return FolderRecursiveReaderComponent(folder).operation()
