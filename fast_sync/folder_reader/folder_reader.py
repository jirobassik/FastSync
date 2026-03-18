from pathlib import Path

from .base import Reader
from .folder_filter_reader import FolderRecursiveReaderComponent


class FolderReader(Reader):
    def __repr__(self):
        return self.__class__.__name__

    def read(self, folder: Path):
        return FolderRecursiveReaderComponent(folder).operation()
