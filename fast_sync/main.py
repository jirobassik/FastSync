from pathlib import Path

from fast_sync import DiffFolder, FolderSync, HashContentFolder

first_folder = "/home/puzer/OS_emulate/Music2"
second_folder = "/home/puzer/OS_emulate/Music3"
medium_folder1 = "/home/puzer/OS_emulate/Music_medium2"
medium_folder2 = "/home/puzer/OS_emulate/Music_medium3"
hard_folder = "/home/puzer/OS_emulate/Music"


class SyncManager:
    hash_content_folder = HashContentFolder
    folder_sync = FolderSync

    def __init__(self, left_folder, right_folder):
        self.left_path = Path(left_folder)
        self.right_path = Path(right_folder)

        # self.hash_content_folder = self.hash_content_folder()

        self.left_hash = self.hash_content_folder().create_hash(self.left_path)
        self.right_hash = self.hash_content_folder().create_hash(self.right_path)

        self.diff_folder = DiffFolder(self.left_hash, self.right_hash)
        self.file_sync = self.folder_sync(self.left_path, self.right_path, self.diff_folder)

    def left_missing_paths(self):
        return self.diff_folder.missing_left_dict.values()

    def right_missing_paths(self):
        return self.diff_folder.missing_right_dict.values()

    def view_res(self):
        # self.statistic(self.left_hash)
        # self.statistic(self.right_hash)
        # self.statistic(self.compare1(self.left_hash, self.right_hash))
        # print("------------------------------------------------------")
        # self.statistic(self.compare1(self.right_hash, self.left_hash))
        # self.file_sync.left_sync()
        print(self.diff_folder.missing_left_dict)

    @staticmethod
    def statistic(iter_hashes):
        counter = 0
        for el in iter_hashes:
            print(el)
            if el is not None:
                counter += 1
        print("num hashes: ", counter)
        # set_hashes = set(iter_hashes)
        # print("set hashes", set_hashes, len(set_hashes))
