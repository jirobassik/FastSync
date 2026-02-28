import os
from pathlib import Path

from click import get_app_dir, get_current_context
from click_extra import ConfigOption
from click_extra.decorators import decorator_factory, option

from fast_sync.utils.constant import APP_NAME


class CliNameConfigOption(ConfigOption):
    def default_pattern(self) -> str:
        ctx = get_current_context()
        cli_name = ctx.find_root().info_name
        if not cli_name:
            raise ValueError
        app_dir = Path(
            get_app_dir(APP_NAME, roaming=self.roaming, force_posix=self.force_posix),
        ).resolve()
        return f"{app_dir}{os.path.sep}{self.file_pattern}"


config_option = decorator_factory(dec=option, cls=CliNameConfigOption)
