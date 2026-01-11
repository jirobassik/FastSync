from pathlib import Path

import click

from cli.utils.output_formaters.formaters import grouped_output, echo_files, sorted_output


class OutputFormater:

    def __init__(self, sorted_=False, grouped=False):
        self.sorted_ = sorted_
        self.grouped = grouped

    def __call__(self, dict_values_missing: list[Path], folder=None):
        if dict_values_missing:
            click.secho(f"Total missing 📄: {len(dict_values_missing)}", fg="yellow")
            if self.sorted_:
                sorted_output(dict_values_missing)
            if self.grouped:
                grouped_output(dict_values_missing, folder)
            elif not self.grouped and not self.sorted_:
                echo_files(dict_values_missing)
        else:
            click.secho("No missing files", fg="green")
