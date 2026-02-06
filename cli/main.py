import click
from loguru import logger

from cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync import FolderReader
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)
from fast_sync.folder_reader.folder_filter_reader.folder_filter_reader import (
    FolderFilterReader,
)
from fast_sync.utils.error import NotValidFilterInput

from .utils import CustomHelp, ProgressBarFastSync, error_output


@click.group(cls=CustomHelp)
@click.option("--group", "-g", is_flag=True, help="Group files by folders [Affects the output format]")
@click.option("--sort", "-s", is_flag=True, help="Sort files by name [Affects the output format]")
@click.option("--extensions", "-e", default=(), multiple=True, help="Filter files by extension")
@click.option("--folders", "-f", default=(), multiple=True, help="Exclude files based on folder")
@click.pass_context
def fast_sync_cli(ctx, group, sort, extensions, folders):
    ctx.meta["output_formater"] = OutputFormater(grouped=group, sorted_=sort)

    click.echo("---" * 30)
    click.secho("Fast sync started", fg="green", bold=True)
    try:
        reader = FolderReader()
        if extensions or folders:
            reader = FolderFilterReader(
                FilterFolders(*folders),
                FilterExtensionsFolder(*extensions),
            )

        progress_bar_sync_manager = ProgressBarFastSync(reader)
    except NotValidFilterInput:
        logger.debug("Not valid filter input")
        error_output(
            "Not valid filter input", fix="view examples 'fast_sync.py --help'"
        )
    else:
        ctx.obj = progress_bar_sync_manager
    click.echo("---" * 30)
