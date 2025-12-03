import click
from fast_sync.main import SyncManager
from cli import CustomHelp


@click.group(cls=CustomHelp)
@click.option('--left-folder', '-left', '-l', type=click.Path(exists=True, file_okay=False))
@click.option('--right-folder', '-right', '-r', type=click.Path(exists=True, file_okay=False))
@click.pass_context
def fast_sync(ctx, left_folder, right_folder):
    click.secho("Fast sync started", fg='green', bold=True)
    ctx.obj = SyncManager(left_folder, right_folder)
    click.echo("---" * 30)
