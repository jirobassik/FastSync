import sys
from itertools import chain
from typing import Any, Optional

import click
from click import ClickException, FileError, secho
from click_extra import ExtraContext, ExtraGroup, HelpExtraFormatter
from click_extra.colorize import Style, highlight

from fast_sync.cli.utils.custom_group.examples import ExamplesCli
from fast_sync.cli.utils.error.errors import PermissionDeniedError
from fast_sync.utils.errors import (
    CacheFolderCreationError,
    EqualResolverError,
    HashContentFolderError,
    OsPathResolverError,
)


class CustomGroup(ExtraGroup):
    def __init__(
        self,
        command_examples: Optional[tuple[ExamplesCli, ...]] = None,
        *args,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.command_examples = command_examples

    def __call__(self, *args, **kwargs):
        error = None
        try:
            super().__call__(*args, **kwargs)
        except PermissionError as e:
            error = PermissionDeniedError(e.filename, hint="Permission denied")
        except (FileNotFoundError, ValueError, TypeError) as e:
            error = ClickException(e.__str__())

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
            secho(e, fg="green", bold=True)

        if error is not None:
            self.show_error(error)

    def format_help(self, ctx: ExtraContext, formatter: HelpExtraFormatter):
        super().format_help(ctx, formatter)
        self.format_examples(formatter)

    def format_examples(self, formatter: HelpExtraFormatter):
        if self.command_examples is not None:
            with formatter.section("Examples"):
                CustomHelpFormatter().write_many_examples(
                    formatter, *self.command_examples
                )

    @staticmethod
    def show_error(error: ClickException):
        error.show()
        sys.exit(error.exit_code)


class CustomHelpFormatter(HelpExtraFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.additional_length = 10
        self.cli_structure = get_cli_structure()
        self.coloring = {
            "red": ["fs"],
            "green": self.cli_structure["commands"],
            "bright_yellow": self.cli_structure["options"],
        }

    def write_many_examples(self, formatter: HelpExtraFormatter, *args: ExamplesCli):
        for examples_text in args:
            self.write_example(formatter, examples_text.text, examples_text.explaining)

    def write_example(
        self, formatter: HelpExtraFormatter, text: str, explaining: Optional[str] = None
    ):
        if explaining is not None:
            self.write_explaining(explaining, formatter)

        self.write_command(text, formatter)
        formatter.write_paragraph()

    def write_explaining(self, explaining: str, formatter: HelpExtraFormatter):
        styled_explaining = Style(bold=True, italic=True)(explaining)
        self.change_additional_width(styled_explaining, formatter)

        formatter.write_text(styled_explaining)

    def write_command(self, text: str, formatter: HelpExtraFormatter):
        for color, patterns in self.coloring.items():
            text = highlight(text, patterns=patterns, styling_func=Style(color))
        self.change_additional_width(text, formatter)

        formatter.write_text(text)

    def change_additional_width(self, text: str, formatter: HelpExtraFormatter):
        formatter.width = len(text) + self.additional_length


def get_cli_structure():
    from fast_sync.cli.main import fast_sync_cli

    cli_structure = {"commands": set(), "options": set()}
    # noinspection PyTypeChecker
    ctx: click.Group = click.Context(fast_sync_cli).command

    def _get_cli_structure(sub_ctx):
        if isinstance(sub_ctx, click.Group):
            for name, value in sub_ctx.commands.items():
                cli_structure["commands"].add(name)
                _get_cli_structure(value)

        if isinstance(sub_ctx, click.Command):
            params_opts = [
                option.opts
                for option in sub_ctx.params
                if isinstance(option, click.Option)
            ]
            chain_opts = chain.from_iterable(params_opts)
            cli_structure["options"].update(chain_opts)

        return cli_structure

    return _get_cli_structure(ctx)
