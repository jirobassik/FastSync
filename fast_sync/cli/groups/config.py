import click

from fast_sync.cli.main import fast_sync_cli
from fast_sync.cli.utils.default_config_creation import path_to_config, write_config
from fast_sync.cli.utils.error.errors import ConfigFileCreationError
from fast_sync.cli.utils.output_formaters.formaters import white_bolt_text


@fast_sync_cli.group(name="config-manage", help="Manage config file")
def config():
    pass


@config.command(name="init", help="Init config file")
def init():
    try:
        write_config()
        click.secho(
            f" ✅ Successful create 'config.toml' at the following path: {white_bolt_text(path_to_config())}",
            fg="green",
        )
    except ConfigFileCreationError as e:
        raise click.exceptions.FileError(filename=e.filename, hint=e.message)


@config.command(name="open", help="Open config file")
def open_():
    click.launch(path_to_config().as_uri())
