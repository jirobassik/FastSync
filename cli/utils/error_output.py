import click
from cli.utils.line_wrapper import line_wrapper

@line_wrapper(type_line="*")
def error_output(error, explanation=None, fix=None):
    click.echo(f"{click.style("Error", fg='red')}: {error}")
    detailed_output(explanation, fix)

@line_wrapper(type_line="*", num_lines=35)
def warning_output(warning, explanation=None, fix=None):
    click.echo(f"{click.style("Warning", fg='yellow')}: {warning}")
    detailed_output(explanation, fix)


def detailed_output(explanation, fix):
    if explanation:
        click.echo(f"{explanation}")
    if fix:
        click.echo(f"{click.style("Fix with", fg='green')}: {fix}")
