from pathlib import Path
from typing import ValuesView

import inquirer
from inquirer.themes import GreenPassion, Theme

from fast_sync.duplicate_resolver.duplicate_questions.questions import (
    EqualByYearQuestion,
    EqualGroupByHashQuestion,
)


class EqualMethodQuestion:
    def __init__(self, theme: Theme = GreenPassion()):
        self.theme = theme

    def __repr__(self):
        return f"{self.__class__.__name__}theme={self.theme})"

    def start_questions(self, duplicates: ValuesView[list[Path]]):
        choose_method_question = [
            inquirer.List(
                "choose_method",
                message="Choose method for resolve duplicated files",
                choices=[
                    ("Grouped", EqualGroupByHashQuestion(duplicates, self.theme)),
                    ("Year", EqualByYearQuestion(duplicates, self.theme)),
                ],
            ),
        ]
        answers = inquirer.prompt(
            choose_method_question, raise_keyboard_interrupt=True, theme=self.theme
        )

        choosed_files = answers.get("choose_method").get_duplicates()
        return choosed_files
