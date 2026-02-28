import click

from fast_sync.cli.main import fast_sync_cli
from fast_sync.cli.utils.default_config_creation import path_to_config, write_config
from fast_sync.cli.utils.errors import ConfigFileCreationError


@fast_sync_cli.group(name="config-manage", help="Manage config file")
def config():
    pass


@config.command(name="init", help="Init config file")
def init():
    try:
        write_config()
    except ConfigFileCreationError as e:
        raise click.exceptions.FileError(
            filename=getattr(e, "filename"), hint="Permission error"
        )


@config.command(name="open", help="Open config file")
def open_():
    click.launch(path_to_config().as_uri())
