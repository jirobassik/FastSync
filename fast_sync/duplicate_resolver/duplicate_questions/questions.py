from itertools import chain
from pathlib import Path
from typing import Generator, ValuesView

import inquirer
from inquirer.questions import Question
from inquirer.themes import Theme

from fast_sync.duplicate_resolver.duplicate_filtering import (
    FilterDuplicateByDateCreationTime,
)
from fast_sync.duplicate_resolver.duplicate_questions.base import (
    BaseQuestion,
)


class EqualGroupQuestion(BaseQuestion):
    def __init__(self, duplicates: ValuesView[list[Path]], theme: Theme):
        super().__init__(duplicates, theme)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(duplicates={self.duplicates},"
            f"theme={self.theme})"
        )

    def get_duplicates(self):
        return self.answer()

    def answer(self) -> Generator:
        answers = inquirer.prompt(
            self.question(), raise_keyboard_interrupt=True, theme=self.theme
        )

        chained_from_answers = chain.from_iterable(answers.values())
        return chained_from_answers

    def question(self) -> list[Question]:
        raise NotImplementedError


class FilterDuplicateByCheckboxQuestion(EqualGroupQuestion):
    def __repr__(self):
        return f"{self.__class__.__name__}"

    def question(self):
        questions = [
            inquirer.Checkbox(
                f"Group number {ind + 1}",
                message="Dublicates files. Choose to delete",
                choices=dublicate,
                carousel=True,
            )
            for ind, dublicate in enumerate(self.duplicates)
        ]
        return questions


class FilterDuplicateByDateCreationTimeQuestion(BaseQuestion):
    def __init__(self, duplicates: ValuesView[list[Path]], theme: Theme):
        super().__init__(duplicates, theme)

    def __repr__(self):
        return f"{self.__class__.__name__}(duplicates={self.duplicates})"

    def get_duplicates(self):
        return self.answer()

    def answer(self):
        answers = inquirer.prompt(
            self.question(), raise_keyboard_interrupt=True, theme=self.theme
        )
        return FilterDuplicateByDateCreationTime(
            filter_by=answers.get("choose_filter_date")
        ).filter_duplicate(self.duplicates)

    def question(self):
        choose_filter_method = [
            inquirer.List(
                "choose_filter_date",
                message="Delete dublicates files",
                choices=[
                    ("Newest", "newest"),
                    ("Oldest", "oldest"),
                ],
            )
        ]
        return choose_filter_method
