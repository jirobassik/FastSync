import click
from click import Context, HelpFormatter, wrap_text

from fast_sync.cli.utils.custom_help.examples import examples_cli, examples


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


class CustomHelp(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help(ctx, formatter)
        self.format_examples(ctx, formatter)

    @staticmethod
    def format_examples(ctx: Context, formatter: HelpFormatter) -> None:
        with formatter.section("EXAMPLES"):
            CustomHelpFormatter().write_many_examples(formatter, *examples)
