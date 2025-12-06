import shutil
from pathlib import Path

from fast_sync import DiffFolder


class FolderSync:
    def __init__(self, left_path, right_path, diff_folder: DiffFolder):
        self.left_path = left_path
        self.right_path = right_path
        self.diff_folder = diff_folder

    def left_sync(self):
        self._sync(self.right_path, self.left_path, self.diff_folder.missing_left_dict)

    def right_sync(self):
        self._sync(self.left_path, self.right_path, self.diff_folder.missing_right_dict)

    def _sync(self, source_folder, destination_folder, missing_files):
        files_to_copy = list(missing_files.values()) #FIXME Может в будущем аукнуться
        for missing_file in files_to_copy:
            self.folder_sync(source_folder, destination_folder, missing_file)

    @staticmethod
    def folder_sync(source_folder, destination_folder, missing_file):
        missing_file_path = missing_file.relative_to(source_folder)
        destination_sync_folder = Path(destination_folder, missing_file_path)
        destination_sync_folder.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(missing_file, destination_sync_folder)