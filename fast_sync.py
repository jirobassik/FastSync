from multiprocessing import freeze_support

from fast_sync.cli.main import fast_sync_cli
from fast_sync.cli.utils.custom_group.custom_theme import custom_theme
from fast_sync.utils.logging_config import setup_logging

if __name__ == "__main__":
    freeze_support()
    setup_logging()
    fast_sync_cli(formatter_settings={"width": 100, "theme": custom_theme()})
