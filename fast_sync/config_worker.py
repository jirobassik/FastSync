import tomllib
from pathlib import Path

path_to_config = Path("config.toml").absolute()


def get_ext():
    with open(path_to_config, "rb") as f:
        data = tomllib.load(f)
    return data["options"]["filter_extensions"]
