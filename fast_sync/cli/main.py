from typing import NamedTuple
import click
import click_extra
from click_extra import ExtraContext

from fast_sync.cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync.configures import hash_configure, reader_configure
from fast_sync.containers.progressbar_container import ProgressBarContainer
from fast_sync.duplicate_resolver.duplicate_resolver import DuplicateResolver
from fast_sync.main import FastSync
from fast_sync.utils.num_process import number_of_usable_cpus

from .utils import CustomGroup
from .utils.custom_config_option import config_option
from .utils.custom_group.examples import command_examples_fast_sync_cli
from .utils.constant import CLI_NAME


class CliApplicationsObj(NamedTuple):
    fast_sync: FastSync
    duplicate_resolver: DuplicateResolver


@click.group(name=CLI_NAME, cls=CustomGroup, command_examples=command_examples_fast_sync_cli)
@click_extra.option("--caching/--no-caching", "-ch/-Nch", default=False, help="Use cache for boost repeat calculations (Warning if the files "
                                                 "have the same name and different contents --caching, "
                                                 "caching should not be used in this case).")
@click_extra.option("--group/--no-group", "-g/-Ng", default=False, help="Group files by folders (Affects the output format).")
@click_extra.option("--sort/--no-sort", "-s/-Ns", default=False, help="Sort files by name (Affects the output format).")
@click_extra.option("--num-processes", "-np", default=2, type=click_extra.IntRange(1, number_of_usable_cpus()), help="Number of dedicated processes for file processing. Change only at your own risk.")
@click_extra.option("--extensions", "-e", default=(), multiple=True, help="Filter files by extension. Example: `-e '.mp3'`.")
@click_extra.option("--folders", "-f", default=(), multiple=True, help="Exclude files based on folder.")
@click_extra.color_option
@config_option(strict=True, roaming=False)
@click_extra.no_config_option
@click_extra.pass_context
def fast_sync_cli(
    ctx: ExtraContext,
    caching: bool,
    group: bool,
    sort: bool,
    num_processes: int,
    extensions: tuple[str, ...],
    folders: tuple,
):
    click_extra.echo("---" * 30)
    click_extra.secho("Fast sync started", fg="green", bold=True)

    ctx.meta["output_formater"] = OutputFormater(
        grouped=group, sorted_=sort, num_processes=num_processes, caching=caching, extensions=extensions, folders=folders
    )

    # Define main container
    fast_sync_container = ProgressBarContainer

    # Get reader and hash method from user options values
    reader_method = reader_configure(fast_sync_container, extensions, folders).value
    hash_method = hash_configure(fast_sync_container, caching, num_processes).value

    fast_sync_container_instance = fast_sync_container(
        reader_type=reader_method, hash_type=hash_method
    )

    fast_sync_progress_bar = fast_sync_container_instance.fast_sync()
    duplicate_resolver_progress_bar = fast_sync_container_instance.duplicate_resolver()

    fast_sync_application = fast_sync_progress_bar.fast_sync_application()
    duplicate_resolver_application = (
        duplicate_resolver_progress_bar.duplicate_resolver_application()
    )

    ctx.obj = CliApplicationsObj(
        fast_sync=fast_sync_application,
        duplicate_resolver=duplicate_resolver_application,
    )
    click.echo("---" * 30)
