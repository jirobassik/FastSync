from pathlib import Path

from fast_sync import DiffFolder, FolderSync, HashContentFolder, FolderReader, FolderFilterReader
from fast_sync.utils.error import SyncManagerError


class PathConfig:
    __slots__ = ("_left_folder", "_right_folder")

    def __init__(self, left_folder: str, right_folder: str):
        self._left_folder = Path(left_folder)
        self._right_folder = Path(right_folder)

    @property
    def left_folder(self) -> Path:
        return self._left_folder

    @property
    def right_folder(self) -> Path:
        return self._right_folder


class SyncManager(PathConfig):
    hash_content_folder = HashContentFolder
    folder_sync_ = FolderSync

    def __init__(self, left_folder: str, right_folder: str, reader: FolderReader | FolderFilterReader):
        super().__init__(left_folder, right_folder)
        self._hash_content_folder = type(self).hash_content_folder(reader=reader)
        self._diff_folder = None
        self._folder_sync = None
        self._is_analyzed = False

    def analyze(self):
        if not self._is_analyzed:
            self._hash_content_folder.calculate_hash(self.left_folder, self.right_folder)
            self._diff_folder = DiffFolder(
                self._hash_content_folder.left_hash,
                self._hash_content_folder.right_hash
            )
            self._is_analyzed = True

    def reanalyze(self):
        self._is_analyzed = False
        self.analyze()

    def prepare_sync(self):
        self.analyze()
        self._folder_sync = type(self).folder_sync_(self._left_folder, self._right_folder, self._diff_folder)

    @property
    def diff_folder(self) -> DiffFolder:
        if self._diff_folder is None:
            raise SyncManagerError("Call analyze() method first")
        return self._diff_folder

    @property
    def folder_sync(self) -> FolderSync:
        if self._folder_sync is None:
            raise SyncManagerError("Call analyze() method first")
        return self._folder_sync
