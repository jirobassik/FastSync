import click

from cli.main import fast_sync_cli
from cli.utils import echo_files
from fast_sync.main import SyncManager


@fast_sync_cli.group(help="View missing files in chosen folder")
def missing():
    pass


@missing.command('left', short_help="Missing files in left folder")
@click.pass_obj
def view_left_missing(obj: SyncManager):
    click.echo(f"Missing in folder: {obj.left_folder}")
    echo_files(obj.left_missing_files())


@missing.command('right', short_help="Missing files in right folder")
@click.pass_obj
def view_right_missing(obj: SyncManager):
    click.echo(f"Missing in folder: {obj.right_folder}")
    echo_files(obj.right_missing_files())
