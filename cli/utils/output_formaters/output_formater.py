from pathlib import Path

import click

from cli.utils.output_formaters.errors import OutputFormaterError
from cli.utils.output_formaters.formaters import (
    echo_files,
    grouped_output,
    sorted_output,
    white_bolt_text,
)


class OutputFormater:
    def __init__(self, sorted_=False, grouped=False):
        self.sorted_ = sorted_
        self.grouped = grouped

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
