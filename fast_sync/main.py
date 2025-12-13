from pathlib import Path

from fast_sync import DiffFolder, FolderSync, HashContentFolder


class SyncManager:
    hash_content_folder = HashContentFolder
    folder_sync = FolderSync

    def __init__(self, left_folder, right_folder):
        self.left_path = Path(left_folder)
        self.right_path = Path(right_folder)

        self.left_hash = self.hash_content_folder().create_hash(self.left_path)
        self.right_hash = self.hash_content_folder().create_hash(self.right_path)

        self.diff_folder = DiffFolder(self.left_hash, self.right_hash)
        self.file_sync = self.folder_sync(
            self.left_path, self.right_path, self.diff_folder
        )

    def left_missing_paths(self):
        return self.diff_folder.missing_left_dict.values()

    def right_missing_paths(self):
        return self.diff_folder.missing_right_dict.values()
