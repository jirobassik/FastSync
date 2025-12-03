import click


def line_wrapper(func, num_lines: int = 30):
    def wrapper(*args, **kwargs):
        click.echo("---" * num_lines)
        func(*args, **kwargs)
        click.echo("---" * num_lines)

    return wrapper


@line_wrapper
def echo_files(files: list):
    if files:
        for file in files:
            click.echo(file)
    else:
        click.secho("No missing files", fg="green")
