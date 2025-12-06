import click

from cli.utils import echo_files
from cli.main import fast_sync
from fast_sync.main import SyncManager


@fast_sync.group(help="View missing files in choose folder")
def missing():
    pass


@missing.command('left', short_help="Missing files in left folder")
@click.pass_obj
def view_left_missing(obj: SyncManager):
    click.echo(f"Missing in folder: {obj.left_path}")
    echo_files(obj.left_missing_paths())


@missing.command('right', short_help="Missing files in right folder")
@click.pass_obj
def view_right_missing(obj: SyncManager):
    click.echo(f"Missing in folder: {obj.right_path}")
    echo_files(obj.right_missing_paths())
