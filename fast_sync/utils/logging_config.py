import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from platformdirs import PlatformDirs

from fast_sync.utils.constant import APP_NAME

load_dotenv()

default_path_to_log: Path = PlatformDirs(
    appname=APP_NAME, appauthor=False
).user_log_path


def setup_logging():
    logger.remove()

    dev_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    prod_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    if os.getenv("ENV_TYPE", "debug") == "debug":
        logger.add(sys.stderr, level="DEBUG", format=dev_format, colorize=True)
        logger.info("Development mode: logging is configured to output to the console.")
    else:
        logger.add(sys.stderr, level="INFO", format=prod_format, colorize=False)

        logger.add(
            f"{default_path_to_log}/app.log",
            level="DEBUG",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            serialize=True,
        )
        logger.info(
            f"Production mode: logging is configured to output to file and console.\nPath to log file: {default_path_to_log}"
        )
