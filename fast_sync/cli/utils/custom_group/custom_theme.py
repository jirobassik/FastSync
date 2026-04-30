from click_extra import HelpExtraTheme
from cloup import Color, Style


def custom_theme() -> HelpExtraTheme:
    return HelpExtraTheme(
        invoked_command=Style(fg=Color.bright_white),
        heading=Style(fg=Color.bright_blue, bold=True, underline=True),
        constraint=Style(fg=Color.magenta),
        alias=Style(fg=Color.cyan),
        # Style aliases punctuation like options, but dimmed.
        alias_secondary=Style(fg=Color.cyan, dim=True),
        ### Click Extra styles.
        option=Style(fg=Color.cyan),
        # Style subcommands like options and aliases.
        subcommand=Style(fg=Color.yellow),
        choice=Style(fg=Color.magenta),
        metavar=Style(fg=Color.cyan, dim=True),
        bracket=Style(dim=True),
        envvar=Style(fg=Color.yellow, dim=True),
        default=Style(fg=Color.green, dim=True, italic=True),
        deprecated=Style(fg=Color.bright_yellow, bold=True),
        search=Style(fg=Color.green, bold=True),
        success=Style(fg=Color.green),
        ### Non-canonical Click Extra styles.
        subheading=Style(fg=Color.blue),
    )
