from cli.main import fast_sync
from logging_config import setup_logging

setup_logging()

if __name__ == "__main__":
    fast_sync()

# from fast_sync import SyncManager
#
# first_folder = "/home/puzer/OS_emulate/Small music1"
# second_folder = "/home/puzer/OS_emulate/Small_music2"
# medium_folder1 = "/home/puzer/OS_emulate/Music_medium2"
# medium_folder2 = "/home/puzer/OS_emulate/Music_medium3"
# hard_folder = "/home/puzer/OS_emulate/Music"
# SyncManager(first_folder, second_folder).view_res()
