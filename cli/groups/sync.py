import click
from cli.main import fast_sync
from fast_sync.main import SyncManager


@fast_sync.group(help="Sync folders")
def sync():
    pass


@sync.command('left', short_help="Sync left folder with right folder")
@click.confirmation_option(prompt='Are you sure you want to sync left folder with right folder?')
@click.pass_obj
def view_left_missing(obj: SyncManager):
    click.echo(f"Syncing folder: {obj.left_path} with {obj.right_path}")
    #TODO Добавить прогрессбар
    obj.file_sync.left_sync()
    click.echo(f"Successful syncing folder: {obj.left_path} with {obj.right_path}")


@sync.command('right', short_help="Sync right folder with left folder")
@click.confirmation_option(prompt='Are you sure you want to sync right folder with left folder?')
@click.pass_obj
def view_right_missing(obj: SyncManager):
    click.echo(f"Syncing folder: {obj.right_path} with {obj.left_path}")
    obj.file_sync.right_sync()
    click.echo(f"Successful syncing folder: {obj.right_path} with {obj.left_path}")
