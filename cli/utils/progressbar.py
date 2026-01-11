import multiprocessing
from functools import partial
from pathlib import Path

from tqdm import tqdm

from fast_sync import HashContentFolder, FolderSync, FastSync
from fast_sync.utils.types import ListHashPathKeyValue


class ProgressBarHashContentFolder(HashContentFolder):
    def _create_hash(self, path_to_main_folder: Path) -> ListHashPathKeyValue:
        results = []
        with multiprocessing.Pool() as pool:
            with tqdm(desc=f"Creating hash: {path_to_main_folder}") as pbar:
                hash_path_add_path_to_main_folder = partial(self._hash_path, path_to_main_folder=path_to_main_folder)
                for result in pool.imap_unordered(
                        hash_path_add_path_to_main_folder, self._reader.operation(path_to_main_folder)
                ):
                    results.append(result)
                    pbar.update(1)
        return results


class ProgressBarFolderSync(FolderSync):
    def _sync(self, source_folder, destination_folder, missing_files):
        files_to_copy = missing_files.values()
        progressbar_missing_files = tqdm(
            files_to_copy,
            total=len(files_to_copy),
            desc="Copying files",
            unit="file",
            position=0,
            leave=True,
        )
        for missing_file in progressbar_missing_files:
            self.folder_sync(source_folder, destination_folder, missing_file)


class ProgressBarFastSync(FastSync):
    hash_content_folder = ProgressBarHashContentFolder
    folder_sync_ = ProgressBarFolderSync
