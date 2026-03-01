from itertools import groupby
from pathlib import Path

import click

from fast_sync.cli.utils.line_wrapper import line_wrapper, group_line_wrapper


@line_wrapper(type_line="*", num_lines=35)
def echo_files(files: list):
    for file in files:
        click.echo(file.name)


def sorted_output(missing_files: list[Path]):
    echo_files(sorted(missing_files))


def white_bolt_text(text: str | int | Path):
    return click.style(text, fg="white", bold=True)


@group_line_wrapper(type_line="─", num_lines=100)
def grouped_output(missing_files: list[Path], folder):
    sorted_paths = sorted(missing_files, key=lambda x: x.parent)
    # Группируем по родительским папкам
    for parent, group in groupby(sorted_paths, key=lambda x: x.parent):
        # Получаем уровень вложенности
        level = len(parent.relative_to(folder).parts)
        indent = "│   " * (level - 1) + "├── " if level > 0 else ""

        click.echo(f"{indent}📁 {parent.name}/" if level > 0 else f"📁 {parent.name}/")

        # Отображаем файлы в этой папке
        files = list(group)
        for i, file in enumerate(sorted(files, key=lambda x: x.name)):
            is_last = i == len(files) - 1
            file_indent = "│   " * level + ("└── " if is_last else "├── ")
            click.echo(f"{file_indent}📄 {file.name}")
