import shutil
from pathlib import Path

from fast_sync import DiffFolder


class FolderSync:
    __slots__ = ("_left_path", "_right_path", "_diff_folder")

    def __init__(self, left_path: Path, right_path: Path, diff_folder: DiffFolder):
        self._left_path = left_path
        self._right_path = right_path
        self._diff_folder = diff_folder

    def left_sync(self):
        self._sync(self._right_path, self._left_path, self._diff_folder.missing_left_dict)

    def right_sync(self):
        self._sync(self._left_path, self._right_path, self._diff_folder.missing_right_dict)

    def _sync(self, source_folder, destination_folder, missing_files):
        files_to_copy = missing_files.values()
        for missing_file in files_to_copy:
            self.folder_sync(source_folder, destination_folder, missing_file)

    @staticmethod
    def folder_sync(source_folder, destination_folder, missing_file):
        missing_file_path = missing_file.relative_to(source_folder)
        destination_sync_folder = Path(destination_folder, missing_file_path)
        destination_sync_folder.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(missing_file, destination_sync_folder)