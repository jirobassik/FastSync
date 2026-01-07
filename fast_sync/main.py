from fast_sync.sync_manager import SyncManager


class FastSync(SyncManager):
    def left_missing_files(self):
        return self.diff_folder.missing_left_dict.values()

    def right_missing_files(self):
        return self.diff_folder.missing_right_dict.values()

    def left_sync_files(self):
        self.folder_sync.left_sync()

    def right_sync_files(self):
        self.folder_sync.right_sync()
