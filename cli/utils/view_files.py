import click

from cli.utils.line_wrapper import line_wrapper


@line_wrapper(type_line="*", num_lines=35)
def echo_files(files: list):
    if files:
        for file in files:
            click.echo(file)
    else:
        click.secho("No missing files", fg="green")
