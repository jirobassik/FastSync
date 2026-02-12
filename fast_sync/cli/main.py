import click
from loguru import logger

from fast_sync import FolderReader
from fast_sync.cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync.folder_reader.folder_filter_reader import (
    FilterExtensionsFolder,
    FilterFolders,
)
from fast_sync.folder_reader.folder_filter_reader.folder_filter_reader import (
    FolderFilterReader,
)
from fast_sync.utils.error import NotValidFilterInput

from .utils import CustomHelp, ProgressBarFastSync, error_output
from .utils.progressbar import ProgressBarHashContentFolderCaching, ProgressBarHashContentFolder


@click.group(cls=CustomHelp)
@click.option("--hashing", "-h", is_flag=True, help="Use hash for boost repeat calculations [Warning if the files "
                                                 "have the same name and different contents, "
                                                 "caching should not be used in this case]")
@click.option("--group", "-g", is_flag=True, help="Group files by folders [Affects the output format]")
@click.option("--sort", "-s", is_flag=True, help="Sort files by name [Affects the output format]")
@click.option("--extensions", "-e", default=(), multiple=True, help="Filter files by extension")
@click.option("--folders", "-f", default=(), multiple=True, help="Exclude files based on folder")
@click.pass_context
def fast_sync_cli(ctx, hashing, group, sort, extensions, folders):
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

        hash_method = ProgressBarHashContentFolder
        if hashing:
            hash_method = ProgressBarHashContentFolderCaching
        progress_bar_sync_manager = ProgressBarFastSync(reader, hash_method)
    except NotValidFilterInput:
        logger.debug("Not valid filter input")
        error_output(
            "Not valid filter input", fix="view examples 'fast_sync.py --help'"
        )
    else:
        ctx.obj = progress_bar_sync_manager
    click.echo("---" * 30)
