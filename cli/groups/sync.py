from itertools import chain

import click
import click_extra

from cli.main import fast_sync_cli
from cli.utils.output_formaters.output_formater import OutputFormater
from fast_sync.main import FastSync


@fast_sync_cli.group(help="Sync chosen folder")
@click.pass_context
def sync(ctx):
    ctx.obj.prepare_sync()


class SyncFabric:
    def __init__(self, direction: str):
        self._direction = direction
        self._opposite_direction = "left" if direction == "right" else "right"

        self._folder = lambda direction_: getattr(self._obj, f"{direction_}_folder")
        self._missing_files = lambda: getattr(self._obj, f"{direction}_missing_files")()
        self._sync_files = lambda: getattr(self._obj, f"{direction}_sync_files")()

        self._required_operations = {"sync_files": self._sync_files_wrap}
        self._optional_operations = {"check_sync": self._recheck_sync, "open_sync_folder": self._open_sync_folder}
        self._all_operations = self._required_operations | self._optional_operations

        self._obj = None
        self._output_formater = None

    def create(self):
        # noinspection PyUnresolvedReferences
        @sync.command(self._direction,
                      short_help=f"Sync {self._direction} folder with {self._opposite_direction} folder")
        @click.option('--view-missing', is_flag=True, help="View missing files")
        @click.option('--check-sync', flag_value='check_sync', help="Check sync status")
        @click.option('--open-sync-folder', flag_value='open_sync_folder',
                      help=f"Open {self._direction} folder in file manager")
        @click.decorators.pass_meta_key("output_formater")
        @click.pass_obj
        def sync_dec(obj: FastSync, output_formater: OutputFormater, view_missing: bool, check_sync: str,
                     open_sync_folder: str):
            self._obj = obj
            self._output_formater = output_formater

            if view_missing:
                self._view_missing_files()

            if click_extra.confirm(
                    text=f"Are you sure you want to sync {self._folder(self._direction).name} with {self._folder(self._opposite_direction).name}?",
                    abort=True):
                self._after_confirm_operations(check_sync, open_sync_folder)

        return sync_dec

    def _view_missing_files(self):
        self._output_formater(missing_files=self._missing_files(),
                              missing_folder=self._folder(self._direction),
                              reference_folder=self._folder(self._opposite_direction))

    def _after_confirm_operations(self, *args):
        extend_args = chain(self._required_operations.keys(), args)
        for operation in extend_args:
            if (call_operation := self._all_operations.get(operation)) is not None:
                call_operation()

    def _sync_files_wrap(self):
        click.echo(
            f"Syncing folder: {self._folder(self._opposite_direction).name} ⟹  {self._folder(self._direction).name}")
        self._sync_files()
        click.echo(
            f"{click.style("Successful syncing folder", fg="green")}:"
            f" {self._folder(self._direction).name} with {self._folder(self._opposite_direction).name}")

    def _recheck_sync(self):
        self._obj.reanalyze()
        click.echo(f"Repeat check 📄 in folder: {self._folder(self._direction).name}")
        self._view_missing_files()

    def _open_sync_folder(self):
        click.launch(self._folder(self._direction).absolute().as_uri())


sync_left_folder = SyncFabric("left").create()
sync_right_folder = SyncFabric("right").create()
