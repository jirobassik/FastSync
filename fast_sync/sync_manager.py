from typing import Optional

from fast_sync import (
    DiffFolder,
    FolderSync,
    HashContentFolder,
)
from fast_sync.hash_content_folder import HashContentFolderCaching
from fast_sync.utils.errors import SyncManagerError
from fast_sync.utils.path_setup import PathSetup


class SyncManager(PathSetup):
    folder_sync_ = FolderSync

    def __init__(
        self,
        hash_method: HashContentFolder | HashContentFolderCaching = HashContentFolder(),
    ):
        self._hash_method = hash_method
        self._diff_folder: Optional[DiffFolder] = None
        self._folder_sync: Optional[FolderSync] = None
        self._is_analyzed = False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(hash_method={self._hash_method}, "
            f"diff_folder={self._diff_folder}, "
            f"folder_sync={self._folder_sync}, "
            f"is_analyzed={self._is_analyzed})"
        )

    def analyze(self):
        if not self._is_analyzed:
            self._hash_method.calculate_hash(self.left_folder, self.right_folder)
            self._diff_folder = DiffFolder(
                self._hash_method.left_hash,
                self._hash_method.right_hash,
            )
            self._is_analyzed = True

    def reanalyze(self):
        self._is_analyzed = False
        self.analyze()

    def prepare_sync(self):
        self.analyze()
        self._folder_sync = type(self).folder_sync_(
            self.left_folder,
            self.right_folder,
            self._diff_folder,
        )

    @property
    def diff_folder(self) -> DiffFolder:
        if self._diff_folder is None:
            raise SyncManagerError("Call `.analyze()` method first")
        return self._diff_folder

    @property
    def folder_sync(self) -> FolderSync:
        if self._folder_sync is None:
            raise SyncManagerError("Call `.prepare_sync()` method first")
        return self._folder_sync
