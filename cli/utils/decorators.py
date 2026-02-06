from functools import wraps

import click


def path_setup_wrapper(func):
    @wraps(func)
    @click.option(
        "--left-folder",
        "-left",
        "-l",
        required=True,
        envvar="LEFT_FOLDER",
        type=click.Path(exists=True, file_okay=False),
    )
    @click.option(
        "--right-folder",
        "-right",
        "-r",
        required=True,
        envvar="RIGHT_FOLDER",
        type=click.Path(exists=True, file_okay=False),
    )
    def path_wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return path_wrapper
