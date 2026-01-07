from pathlib import Path

from fast_sync import DiffFolder, FolderSync, HashContentFolder, FolderReader, FolderFilterReader


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
    folder_sync = FolderSync

    def __init__(self, left_folder: str, right_folder: str, reader: FolderReader | FolderFilterReader):
        super().__init__(left_folder, right_folder)
        self._hash_content_folder = type(self).hash_content_folder(reader=reader).calculate_hash(self.left_folder,
                                                                                                 self.right_folder)

        self._diff_folder = DiffFolder(self._hash_content_folder.left_hash, self._hash_content_folder.right_hash)
        self._folder_sync = type(self).folder_sync(
            self.left_folder, self.right_folder, self._diff_folder
        )

    def update_state(self):
        self._hash_content_folder.calculate_hash(self.left_folder, self.right_folder)
        self._diff_folder = DiffFolder(self._hash_content_folder.left_hash, self._hash_content_folder.right_hash)

    def left_missing_files(self, update=False):
        return self._diff_folder.missing_left_dict.values()

    def right_missing_files(self):
        return self._diff_folder.missing_right_dict.values()

    def left_sync_files(self):
        self._folder_sync.left_sync()

    def right_sync_files(self):
        self._folder_sync.right_sync()
