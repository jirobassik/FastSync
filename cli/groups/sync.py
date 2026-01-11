import click

from cli.main import fast_sync_cli
from cli.utils import echo_files
from fast_sync.main import FastSync


@fast_sync_cli.group(help="Sync folders chosen folder")
@click.pass_context
def sync(ctx):
    ctx.obj.prepare_sync()


# noinspection PyUnresolvedReferences
@sync.command('left', short_help="Sync left folder with right folder")
@click.option('--check-sync', is_flag=True, help="Check sync status")
@click.confirmation_option(prompt='Are you sure you want to sync left folder with right folder?')
@click.pass_obj
def sync_left_folder(obj: FastSync, check_sync: bool):
    click.echo(f"Syncing folder: {obj.left_folder} with {obj.right_folder}")
    obj.left_sync_files()
    click.echo(f"{click.style("Successful syncing folder", fg="green")}: {obj.left_folder} with {obj.right_folder}")
    if check_sync:
        obj.reanalyze()
        echo_files(obj.left_missing_files())


# noinspection PyUnresolvedReferences
@sync.command('right', short_help="Sync right folder with left folder")
@click.option('--check-sync', is_flag=True, help="Check sync status")
@click.confirmation_option(prompt='Are you sure you want to sync right folder with left folder?')
@click.pass_obj
def sync_right_folder(obj: FastSync, check_sync: bool):
    click.echo(f"Syncing folder: {obj.right_folder} with {obj.left_folder}")
    obj.right_sync_files()
    click.echo(f"{click.style("Successful syncing folder", fg="green")}: {obj.right_folder} with {obj.left_folder}")
    if check_sync:
        obj.reanalyze()
        echo_files(obj.right_missing_files())
