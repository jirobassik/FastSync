from contextlib import suppress

import click

from cli.main import fast_sync_cli
from fast_sync.main import SyncManager


@fast_sync_cli.group(help="Sync folders chosen folder")
def sync():
    pass


@sync.command('left', short_help="Sync left folder with right folder")
@click.confirmation_option(prompt='Are you sure you want to sync left folder with right folder?')
@click.pass_obj
def sync_left_folder(obj: SyncManager):
    with suppress(AttributeError):
        click.echo(f"Syncing folder: {obj.left_folder} with {obj.right_folder}")
        obj.left_sync_files()
        click.echo(f"{click.style("Successful syncing folder", fg="green")}: {obj.left_folder} with {obj.right_folder}")


@sync.command('right', short_help="Sync right folder with left folder")
@click.confirmation_option(prompt='Are you sure you want to sync right folder with left folder?')
@click.pass_obj
def sync_right_folder(obj: SyncManager):
    with suppress(AttributeError):
        click.echo(f"Syncing folder: {obj.right_folder} with {obj.left_folder}")
        obj.right_sync_files()
        click.echo(f"{click.style("Successful syncing folder", fg="green")}: {obj.right_folder} with {obj.left_folder}")
