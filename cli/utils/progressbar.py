import multiprocessing
from pathlib import Path

from tqdm import tqdm

from fast_sync import HashContentFolder, FolderSync, SyncManager


class ProgressBarHashContentFolder(HashContentFolder):
    def create_hash(self, pure_path: Path):
        results = []
        with multiprocessing.Pool() as pool:
            with tqdm(desc=f"Creating hash: {pure_path}") as pbar:
                for result in pool.imap_unordered(
                    self._hash_path, self._rglob_filter_pattern_files(pure_path)
                ):
                    results.append(result)
                    pbar.update(1)
        return results


class ProgressBarFolderSync(FolderSync):
    def _sync(self, source_folder, destination_folder, missing_files):
        files_to_copy = list(missing_files.values())
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


class ProgressBarSyncManager(SyncManager):
    hash_content_folder = ProgressBarHashContentFolder
    folder_sync = ProgressBarFolderSync
