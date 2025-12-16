import click


def error_output(error, explanation=None, fix=None):
    click.echo(f"{click.style("Error", fg='red')}: {error}")
    detailed_output(explanation, fix)


def warning_output(warning, explanation=None, fix=None):
    click.echo(f"{click.style("Warning", fg='yellow')}: {warning}")
    detailed_output(explanation, fix)


def detailed_output(explanation, fix):
    if explanation:
        click.echo(f"{explanation}")
    if fix:
        click.echo(f"{click.style("Fix with", fg='green')}: {fix}")
