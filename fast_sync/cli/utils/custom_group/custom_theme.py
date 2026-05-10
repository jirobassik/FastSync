from click_extra import (
    Color,
    HelpExtraTheme,
    Style,
)


def neon():
    return HelpExtraTheme.dark().with_(
        heading=Style(fg=Color.bright_magenta, bold=True, underline=True),
        option=Style(fg=Color.bright_cyan),
        choice=Style(fg=Color.bright_yellow),
        subcommand=Style(fg=Color.bright_green),
    )


def dark():
    return HelpExtraTheme.dark().with_(
        heading=Style(fg=Color.bright_blue, bold=True, underline=True),
        option=Style(fg=Color.cyan),
        choice=Style(fg=Color.magenta),
        subcommand=Style(fg=Color.bright_black),
    )


def light():
    return HelpExtraTheme.light().with_(
        heading=Style(fg=Color.blue, bold=True, underline=True),
        option=Style(fg=Color.bright_blue),
        choice=Style(fg=Color.magenta),
        subcommand=Style(fg=Color.bright_white),
    )
