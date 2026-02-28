import os
from pathlib import Path
from typing import Iterable, Any

import requests
from boltons.urlutils import URL
from click import get_app_dir, get_current_context
from click_extra import ConfigOption
from click_extra.decorators import decorator_factory, option
from extra_platforms import is_windows
from wcmatch import glob, fnmatch

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

    def search_and_read_file(
        self, pattern: str
    ) -> Iterable[tuple[Path | URL, str | bytes]]:
        files_found = 0
        location = URL(pattern)
        location.normalize()
        if location and location.scheme in ("http", "https"):
            with requests.get(str(location)) as response:
                if response.ok:
                    files_found += 1
                    yield location, response.text

        else:
            if is_windows():
                win_path = Path(pattern)
                pattern = str(win_path.as_posix())

            for search_pattern in self.parent_patterns(pattern):
                for file in glob.iglob(search_pattern, flags=self.search_pattern_flags):
                    file_path = Path(file).resolve()
                    if not file_path.is_file():
                        continue
                    files_found += 1
                    yield file_path, file_path.read_bytes()

        if not files_found:
            raise FileNotFoundError(f"No file found matching {pattern}")

    def read_and_parse_conf(
        self,
        pattern: str,
    ) -> tuple[Path | URL, dict[str, Any]] | tuple[None, None]:
        """Search for a parseable configuration file.

        Returns the location and data structure of the first configuration matching the
        ``pattern``.

        Only return the first match that:

        - exists,
        - is a file,
        - is not empty,
        - match file format patterns,
        - can be parsed successfully, and
        - produce a non-empty data structure.

        Raises ``FileNotFoundError`` if no configuration file was found matching the
        criteria above.

        Returns ``(None, None)`` if files were found but none could be parsed.
        """
        for location, content in self.search_and_read_file(pattern):
            if isinstance(location, URL):
                filename = location.path_parts[-1]
            else:
                filename = location.name

            # Match file with formats.
            matching_formats = tuple(
                fmt
                for fmt, patterns in self.file_format_patterns.items()
                if fnmatch.fnmatch(filename, patterns, flags=self.file_pattern_flags)
            )

            if not matching_formats:
                continue

            for conf in self.parse_conf(content, formats=matching_formats):
                if conf:
                    return location, conf

        return None, None


config_option = decorator_factory(dec=option, cls=CliNameConfigOption)
