import os
import sys
from itertools import chain
from typing import Any, Optional

import click
from click import Command, FileError, secho
from click_extra import (
    ClickException,
    ExtraContext,
    ExtraGroup,
    HelpExtraFormatter,
)
from click_extra.colorize import Style, highlight

from fast_sync.cli.utils.custom_group.examples import ExamplesCli
from fast_sync.cli.utils.error.errors import PermissionDeniedError
from fast_sync.utils.errors import (
    CacheFolderCreationError,
    EqualResolverError,
    HashContentFolderError,
    OsPathResolverError,
)


class OverloadFormatterMixin(Command):
    def get_help(self: Command, ctx: click.Context) -> str:
        ctx.formatter_class = ExampleHelpFormatter
        return super().get_help(ctx)


class ErrorHandler:
    def error_handler(self, command, error=None, *args, **kwargs):
        try:
            command(*args, **kwargs)
        except PermissionError as e:
            error = PermissionDeniedError(e.filename, hint="Permission denied")
        except (FileNotFoundError, ValueError, TypeError) as e:
            if os.getenv("ENV_TYPE", "prod") == "debug":
                raise e
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
            self._show_error(error)

    @staticmethod
    def _show_error(error: ClickException):
        error.show()
        sys.exit(error.exit_code)


class CustomGroup(ExtraGroup, OverloadFormatterMixin):
    def __init__(
        self,
        command_examples: Optional[tuple[ExamplesCli, ...]] = None,
        *args,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.command_examples = command_examples

    def __call__(self, *args, **kwargs):
        main_command = super().__call__
        ErrorHandler().error_handler(main_command, *args, **kwargs)

    def format_help(self, ctx: ExtraContext, formatter: ExampleHelpFormatter):
        super().format_help(ctx, formatter)
        self.format_examples(formatter)

    def format_examples(self, formatter: ExampleHelpFormatter):
        if self.command_examples is not None:
            with formatter.section("Examples"):
                formatter.write_many_examples(*self.command_examples)


class ExampleHelpFormatter(HelpExtraFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._additional_length = 10

    def coloring_elements(self) -> dict[str, set[str]]:
        cli_structure = get_cli_structure()
        return {"invoked_command": self.cli_names, **cli_structure}

    def write_many_examples(self, *args: ExamplesCli):
        for examples_text in args:
            self.write_example(examples_text.text, examples_text.explaining)

    def write_example(self, text: str, explaining: Optional[str] = None):
        if explaining is not None:
            self._write_explaining(explaining)

        self._write_command(text)
        self.write_paragraph()

    def _write_explaining(self, explaining: str):
        styled_explaining = Style(bold=True, italic=True)(explaining)
        self._change_additional_width(styled_explaining)

        self.write_text(styled_explaining)

    def _write_command(self, text: str):
        for attr_to_color, patterns in self.coloring_elements().items():
            text = highlight(
                text, patterns=patterns, styling_func=getattr(self.theme, attr_to_color)
            )
        self._change_additional_width(text)
        self.write_text(text)

    def _change_additional_width(self, text: str):
        self.width = len(text) + self._additional_length


def get_cli_structure() -> dict[str, set[str]]:
    from fast_sync.cli.main import fast_sync_cli

    cli_structure = {"subcommand": set(), "option": set()}
    # noinspection PyTypeChecker
    ctx: click.Group = click.Context(fast_sync_cli).command

    def _get_cli_structure(sub_ctx):
        if isinstance(sub_ctx, click.Group):
            for name, value in sub_ctx.commands.items():
                cli_structure["subcommand"].add(name)
                _get_cli_structure(value)

        if isinstance(sub_ctx, click.Command):
            params_opts = (
                option.opts
                for option in sub_ctx.params
                if isinstance(option, click.Option)
            )
            chain_opts = chain.from_iterable(params_opts)
            cli_structure["option"].update(chain_opts)

        return cli_structure

    return _get_cli_structure(ctx)
