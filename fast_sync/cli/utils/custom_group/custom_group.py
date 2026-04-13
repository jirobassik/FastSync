import sys

import click
from click import ClickException, Context, FileError, HelpFormatter, wrap_text

from fast_sync.cli.utils.custom_group.examples import examples, examples_cli
from fast_sync.cli.utils.error.errors import PermissionDeniedError
from fast_sync.utils.errors import (
    CacheFolderCreationError,
    EqualResolverError,
    HashContentFolderError,
    OsPathResolverError,
)


class CustomHelpFormatter(HelpFormatter):
    def write_many_examples(self, formatter: HelpFormatter, *args: examples_cli):
        for examples_text in args:
            self.write_example(formatter, examples_text.text, examples_text.explaining)

    @staticmethod
    def write_example(formatter: HelpFormatter, text, explaining=None):
        formatter.write(
            wrap_text(
                text=text,
                width=100,
                initial_indent="  ",
            )
        )
        formatter.write_paragraph()
        if explaining is not None:
            formatter.write(
                wrap_text(
                    text=explaining,
                    width=100,
                    initial_indent="     ",
                )
            )
            formatter.write_paragraph()


class CustomGroup(click.Group):
    def __call__(self, *args, **kwargs):
        error = None
        try:
            super().__call__(*args, **kwargs)
        except PermissionError as e:
            error = PermissionDeniedError(e.filename, hint="Permission denied")
        except (FileNotFoundError, ValueError, TypeError) as e:
            error = click.exceptions.ClickException(e.__str__())

        except CacheFolderCreationError as e:
            error = PermissionDeniedError(
                e.filename, hint="Try another folder with write and read permissions"
            )
        except OsPathResolverError as e:
            error = FileError(e.filename, hint="Try another path")
        except HashContentFolderError as e:
            error = PermissionDeniedError(
                e.error_class.filename, hint="Permission denied"
            )
        except EqualResolverError as e:
            click.secho(e, fg="green", bold=True)

        if error is not None:
            self.show_error(error)

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help(ctx, formatter)
        self.format_examples(ctx, formatter)

    @staticmethod
    def show_error(error: ClickException):
        error.show()
        sys.exit(error.exit_code)

    @staticmethod
    def format_examples(ctx: Context, formatter: HelpFormatter) -> None:
        with formatter.section("EXAMPLES"):
            CustomHelpFormatter().write_many_examples(formatter, *examples)
