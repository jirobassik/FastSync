import multiprocessing
from functools import partial
from pathlib import Path

from tqdm import tqdm

from fast_sync import FastSync, FolderSync, HashContentFolder, HashContentFolderCaching
from fast_sync.utils.types import ListHashPathKeyValue


class ProgressBarHashContentFolderMixin:
    def _create_hash(
        self: HashContentFolder, path_to_main_folder: Path
    ) -> ListHashPathKeyValue:
        with multiprocessing.Pool() as pool:
            hash_path_add_path_to_main_folder = partial(
                self._hash_path, path_to_main_folder=path_to_main_folder
            )
            result = list(
                tqdm(
                    iterable=pool.imap_unordered(
                        hash_path_add_path_to_main_folder,
                        self._reader.operation(path_to_main_folder),
                    ),
                    desc=f"Creating hash: {path_to_main_folder}",
                    leave=True,
                )
            )

        return result


class ProgressBarFolderSync(FolderSync):
    def _sync(self, source_folder, destination_folder, missing_files):
        files_to_copy = missing_files.values()
        progressbar_missing_files = tqdm(
            files_to_copy,
            desc="Copying files",
            unit="file",
            position=0,
            leave=True,
        )
        for missing_file in progressbar_missing_files:
            self.folder_sync(source_folder, destination_folder, missing_file)


class ProgressBarHashContentFolder(
    ProgressBarHashContentFolderMixin,
    HashContentFolder,
):
    pass


class ProgressBarHashContentFolderCaching(
    ProgressBarHashContentFolderMixin,
    HashContentFolderCaching,
):
    pass


class ProgressBarFastSync(FastSync):
    folder_sync_ = ProgressBarFolderSync
