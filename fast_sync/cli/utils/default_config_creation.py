from pathlib import Path

import tomlkit
from loguru import logger
from platformdirs import PlatformDirs

from fast_sync.cli.utils.constant import CONFIG_DATA
from fast_sync.cli.utils.errors import ConfigFileCreationError
from fast_sync.utils.constant import APP_NAME


def path_to_config() -> Path:
    return PlatformDirs(APP_NAME).user_config_path


def init_config() -> Path:
    config_folder = path_to_config()
    config_folder.mkdir(exist_ok=True)
    return config_folder


def write_config():
    try:
        config_file = init_config().joinpath("config.toml")
        with config_file.open("w", encoding="utf-8") as cf:
            tomlkit.dump(CONFIG_DATA, cf)
    except PermissionError as e:
        logger.error(f"The configuration file was not created. Reason: {e}")
        raise ConfigFileCreationError(filename=e.filename)
    else:
        logger.info(
            f"The configuration file was successfully created at the following path: {config_file}"
        )
