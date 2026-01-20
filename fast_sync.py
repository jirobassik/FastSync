from cli.main import fast_sync_cli
from logging_config import setup_logging

setup_logging()

if __name__ == "__main__":
    fast_sync_cli()
