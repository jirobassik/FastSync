from pathlib import Path
from typing import Optional

import click

from fast_sync.cli.utils.error.errors import OutputFormaterError
from fast_sync.cli.utils.output_formaters.formaters import (
    echo_files,
    grouped_output,
    sorted_output,
    white_bolt_text,
)


class OutputFormater:
    def __init__(
        self,
        sorted_: bool = False,
        grouped: bool = False,
        caching: bool = False,
        num_processes: Optional[int] = None,
        **kwargs,
    ):

        self.sorted_ = sorted_
        self.grouped = grouped

        self.num_processes = num_processes
        self.caching = caching

        self.filters = kwargs

        self._view_user_options()

    def __call__(
        self,
        missing_files: list[Path],
        missing_folder: Path,
        reference_folder: Path = None,
    ):

        if not missing_files:
            click.secho(
                f"\n🗹  No missing files found in {white_bolt_text(missing_folder.name)}",
                fg="green",
            )
            return

        self._summary_missing_output(missing_files)
        self._chooser_output(missing_files, missing_folder.name, reference_folder)

    def _chooser_output(
        self, missing_files: list[Path], missing_folder, reference_folder
    ):
        click.secho(
            f"\n🚫  Missing files in {white_bolt_text(missing_folder)}:", fg="yellow"
        )
        if self.sorted_:
            sorted_output(missing_files)
        if self.grouped:
            self._grouped_output(missing_files, reference_folder)
        elif not self.grouped and not self.sorted_:
            echo_files(missing_files)

    @staticmethod
    def _summary_missing_output(missing_files: list[Path]):
        click.secho(
            f"📊  Total missing files: {white_bolt_text(len(missing_files))}",
            fg="yellow",
            bold=True,
        )

    @staticmethod
    def _grouped_output(missing_files: list[Path], reference_folder):
        if reference_folder is None:
            raise OutputFormaterError("Reference folder not provided")
        grouped_output(missing_files, reference_folder)

    def _view_user_options(self):
        if self.num_processes is not None:
            click.secho(
                f"\nNum processes: {white_bolt_text(self.num_processes)}", fg="green"
            )

        click.secho(
            f"Caching: {white_bolt_text('Yes') if self.caching else white_bolt_text('No')}",
            fg="green",
        )
        self._filters_output()

    def _filters_output(self):
        if any(self.filters.values()):
            click.secho("\nFilters:", fg="green")
            for key, value in self.filters.items():
                if value:
                    click.echo(f" - {white_bolt_text(key)}: {', '.join(value)}")
