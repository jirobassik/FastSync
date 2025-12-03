import click
from click import Context, HelpFormatter


class CustomHelp(click.Group):
    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help(ctx, formatter)
        self.format_examples(ctx, formatter)

    def format_examples(self, ctx: Context, formatter: HelpFormatter) -> None:
        with formatter.section("EXAMPLES"):
            formatter.write_text(
                "All commands are written on one line\n\n"
                "python fast_sync.py -left /home/folder/Music2 -right /Smartphone/DCIM/Music3 missing left\n"
                # FIXME Убрать переход на новую строку
            )
