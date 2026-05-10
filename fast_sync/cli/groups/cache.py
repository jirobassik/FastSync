import click
from click import FileError
from diskcache import Cache

from fast_sync.cli.main import fast_sync_cli
from fast_sync.cli.utils.output_formaters.formaters import white_bolt_text
from fast_sync.hash_content_folder.hash_content_folder_caching.cache_folder_creation import (
    default_path_to_cache,
    exist_file_cache,
)


@fast_sync_cli.group(name="cache", help="Manage cache folder.")
def cache():
    pass


@cache.command(name="init", help="Init cache file.")
def init():
    path_to_cache = default_path_to_cache()
    if not exist_file_cache(path_to_cache):
        Cache(directory=path_to_cache.as_posix())
        click.secho(
            f" ✅ Successful create 'cache.db' at the following path: {white_bolt_text(path_to_cache)}",
            fg="green",
        )
    else:
        click.secho(
            f"File 'cache.db' already exists at the following path: {white_bolt_text(path_to_cache)}",
            fg="green",
        )


@cache.command(name="clear", help="Clear default cache file.")
def clear():
    path_to_cache = default_path_to_cache()
    if not exist_file_cache(path_to_cache):
        raise FileError(
            filename=path_to_cache.as_posix(),
            hint="file cache.db not exists. Use `cache init` for creation",
        )
    Cache(directory=path_to_cache.as_posix()).clear()
    click.secho(
        f"🗑 Clear 'cache.db' at the following path: {white_bolt_text(path_to_cache)}",
        fg="green",
    )


@cache.command(name="open", help="Open default cache folder.")
def open_():
    click.launch(default_path_to_cache().as_uri())
