import click
import click_extra

from cli.main import fast_sync_cli
from fast_sync.main import FastSync


@fast_sync_cli.group(help="Sync chosen folder")
@click.pass_context
def sync(ctx):
    ctx.obj.prepare_sync()


def sync_fabric(direction: str):
    opposite_direction = "left" if direction == "right" else "right"

    folder = lambda obj, direction_: getattr(obj, f"{direction_}_folder")
    missing_files = lambda obj: getattr(obj, f"{direction}_missing_files")
    sync_files = lambda obj: getattr(obj, f"{direction}_sync_files")

    # noinspection PyUnresolvedReferences
    @sync.command(direction, short_help=f"Sync {direction} folder with {opposite_direction} folder")
    @click.option('--view-missing', is_flag=True, help="View missing files")
    @click.option('--check-sync', is_flag=True, help="Check sync status")
    @click.option('--open-sync-folder', is_flag=True, help=f"Open {direction} folder in file manager")
    @click.pass_obj
    def sync_command(obj: FastSync, view_missing: bool, check_sync: bool, open_sync_folder: bool):
        if view_missing:
            click.get_current_context().meta.get("output_formater")(missing_files(obj)(),
                                                                    folder(obj, opposite_direction))

        if click_extra.confirm(
                text=f"Are you sure you want to sync {folder(obj, direction).name} with {folder(obj, opposite_direction).name}?",
                abort=True):
            click.echo(f"Syncing folder: {folder(obj, direction).name} with {folder(obj, opposite_direction).name}")
            sync_files(obj)()

            click.echo(
                f"{click.style("Successful syncing folder", fg="green")}:"
                f" {folder(obj, direction).name} with {folder(obj, opposite_direction).name}")
            if check_sync:
                obj.reanalyze()
                click.get_current_context().meta.get("output_formater")(missing_files(obj)(),
                                                                        folder(obj, opposite_direction))
            if open_sync_folder:
                click.launch(folder(obj, direction).absolute().as_uri())

    return sync_command


sync_left_folder = sync_fabric("left")
sync_right_folder = sync_fabric("right")
