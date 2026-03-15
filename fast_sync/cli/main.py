import click
from click import Context, FileError
from loguru import logger

from fast_sync.cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync.configures import hash_configure, reader_configure
from fast_sync.containers import Container
from fast_sync.utils.errors import (
    CacheFolderCreationError,
    NotValidFilterInput,
    OsPathResolverError,
)

from .utils import CustomHelp, error_output
from .utils.custom_config_option import config_option
from .utils.error.errors import PermissionDeniedError


@click.group(cls=CustomHelp)
@click.option("--hashing/--no-hashing", "-h/-Nh", default=False, help="Use hash for boost repeat calculations [Warning if the files "
                                                 "have the same name and different contents, "
                                                 "caching should not be used in this case]")
@click.option("--group/--no-group", "-g/-Ng", default=False, help="Group files by folders [Affects the output format]")
@click.option("--sort/--no-sort", "-s/-Ns", default=False, help="Sort files by name [Affects the output format]")
@click.option("--extensions", "-e", default=(), multiple=True, help="Filter files by extension")
@click.option("--folders", "-f", default=(), multiple=True, help="Exclude files based on folder")
@config_option(strict=True, roaming=False)
@click.pass_context
def fast_sync_cli(ctx: Context, hashing, group, sort, extensions, folders):
    click.echo("---" * 30)
    click.secho("Fast sync started", fg="green", bold=True)

    ctx.meta["output_formater"] = OutputFormater(
        grouped=group, sorted_=sort, extensions=extensions, folders=folders
    )

    fast_sync_container = Container
    try:
        reader = reader_configure(fast_sync_container, extensions, folders).value
        hash_method = hash_configure(hashing).value

        fast_sync_container_instance = fast_sync_container(
            reader_type=reader, hash_type=hash_method
        )
        fast_sync_progress_bar = fast_sync_container_instance.fast_sync()

    except NotValidFilterInput:
        logger.debug("Not valid filter input")
        error_output(
            "Not valid filter input", fix="view examples 'fast_sync.py --help'"
        )
    except CacheFolderCreationError as e:
        raise PermissionDeniedError(
            e.filename, hint="Try another folder with write and read permissions"
        )
    except OsPathResolverError as e:
        raise FileError(e.filename, hint="Try another path")
    else:
        ctx.obj = fast_sync_progress_bar
    click.echo("---" * 30)
