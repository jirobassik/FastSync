import click

from fast_sync import FolderReader
from fast_sync.folder_reader.folder_filter_reader.folder_filter_reader import FolderFilterReader
from fast_sync.utils.error import NotValidFilterInput
from logging_config import logger
from .utils import CustomHelp, ProgressBarFastSync, error_output


@click.group(cls=CustomHelp)
@click.option('--left-folder', '-left', '-l', required=True, envvar="LEFT_FOLDER",
              type=click.Path(exists=True, file_okay=False))
@click.option('--right-folder', '-right', '-r', required=True, envvar="RIGHT_FOLDER",
              type=click.Path(exists=True, file_okay=False))
@click.option("--extensions", "-e", default=None, multiple=True, help="Filter files by extension")
@click.option("--folders", "-f", default=None, multiple=True, help="Exclude files based on folder")
@click.pass_context
def fast_sync_cli(ctx, left_folder, right_folder, extensions, folders):
    click.echo("---" * 30)
    click.secho("Fast sync started", fg='green', bold=True)
    try:
        reader = FolderReader()
        if extensions or folders:
            reader = FolderFilterReader(extensions, folders)
        progress_bar_sync_manager = ProgressBarFastSync(left_folder, right_folder, reader)
        progress_bar_sync_manager.analyze()
    except NotValidFilterInput:
        logger.debug("Not valid filter input")
        error_output("Not valid filter input", fix="view examples 'fast_sync.py --help'")
    else:
        ctx.obj = progress_bar_sync_manager
    click.echo("---" * 30)
