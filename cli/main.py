import click
from loguru import logger

from .utils import CustomHelp, ProgressBarSyncManager, warning_output


@click.group(cls=CustomHelp)
@click.option('--left-folder', '-left', '-l', type=click.Path(exists=True, file_okay=False))
@click.option('--right-folder', '-right', '-r', type=click.Path(exists=True, file_okay=False))
@click.pass_context
def fast_sync(ctx, left_folder, right_folder):
    click.echo("---" * 30)
    try:
        progress_bar_sync_manager = ProgressBarSyncManager(left_folder, right_folder)
    except TypeError:
        logger.debug("Empty path input")
        warning_output("Empty path input", fix="view examples 'fast_sync.py --help'")
    else:
        click.secho("Fast sync started", fg='green', bold=True)
        ctx.obj = progress_bar_sync_manager
    click.echo("---" * 30)
