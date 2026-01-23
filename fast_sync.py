from multiprocessing import freeze_support

from cli.main import fast_sync_cli
from fast_sync.utils.logging_config import setup_logging

if __name__ == "__main__":
    freeze_support()
    setup_logging()
    fast_sync_cli()
