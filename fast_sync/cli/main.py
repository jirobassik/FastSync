from typing import NamedTuple

import click
from click import Context

from fast_sync.cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync.configures import hash_configure, reader_configure
from fast_sync.containers.progressbar_container import ProgressBarContainer
from fast_sync.duplicate_resolver.duplicate_resolver import EqualResolver
from fast_sync.main import FastSync

from .utils import CustomGroup
from .utils.custom_config_option import config_option


class CliApplicationsObj(NamedTuple):
    fast_sync: FastSync
    equal_resolver: EqualResolver

@click.group(cls=CustomGroup)
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

    # Define main container
    fast_sync_container = ProgressBarContainer

    # Get reader and hash method from user options values
    reader_method = reader_configure(fast_sync_container, extensions, folders).value
    hash_method = hash_configure(hashing).value

    fast_sync_container_instance = fast_sync_container(
        reader_type=reader_method, hash_type=hash_method
    )
    fast_sync_progress_bar = fast_sync_container_instance.fast_sync()
    equal_resolver_progress_bar = fast_sync_container_instance.equal_resolver()

    fast_sync_application = fast_sync_progress_bar.fast_sync_application()
    equal_resolver_application = (
        equal_resolver_progress_bar.equal_resolver_application()
    )

    ctx.obj = CliApplicationsObj(
        fast_sync=fast_sync_application, equal_resolver=equal_resolver_application
    )
    click.echo("---" * 30)
