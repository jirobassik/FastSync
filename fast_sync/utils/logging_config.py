import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


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
            "logs/app.log",
            level="DEBUG",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            serialize=True,
        )
        logger.info(
            "Production mode: logging is configured to output to console and file."
        )
