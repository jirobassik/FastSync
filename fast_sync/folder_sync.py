import shutil
from pathlib import Path

from fast_sync import DiffFolder


class FolderSync:
    def __init__(self, left_path, right_path, diff_folder: DiffFolder):
        self.left_path = left_path
        self.right_path = right_path
        self.diff_folder = diff_folder

    def left_sync(self):
        self.__sync(self.right_path, self.left_path, self.diff_folder.missing_left_dict)

    def right_sync(self):
        self.__sync(self.left_path, self.right_path, self.diff_folder.missing_right_dict)

    @staticmethod
    def __sync(source_folder, destination_folder, missing_files: dict):
        for missing_file in missing_files.values():
            missing_file_path = missing_file.relative_to(source_folder)
            destination_sync_folder = Path(destination_folder, missing_file_path)
            destination_sync_folder.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(missing_file, destination_sync_folder)
