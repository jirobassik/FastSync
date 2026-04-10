import abc
import operator
from functools import reduce
from pathlib import Path
from typing import Generator, Iterable, ValuesView

from loguru import logger

from fast_sync.utils.errors import FilterDublicateByDateCreationTimeError


class FilterDuplicateBase(abc.ABC):
    @abc.abstractmethod
    def filter_duplicate(self, dublicates: ValuesView[list[Path]]) -> Iterable[Path]:
        pass


class FilterDuplicateByDateCreationTime(FilterDuplicateBase):
    __slots__ = ["_date_filtering_method"]

    def __init__(self, filter_by="newest"):
        self._date_filtering_method = self._creation_date_compare_method(filter_by)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"date_filtering_method={self._date_filtering_method})"
        )

    @staticmethod
    def _creation_date_compare_method(filter_by: str):
        try:
            compare_operator = {"newest": operator.gt, "oldest": operator.lt}[filter_by]
        except KeyError:
            logger.error("Not valid `filter_by` value. Supports: `newest`, `oldest`.")
            raise FilterDublicateByDateCreationTimeError(
                "Not valid `filter_by` value. Supports: `newest`, `oldest`."
            )
        else:
            return compare_operator

    def filter_duplicate(self, dublicates: ValuesView[list[Path]]) -> Generator[Path]:
        def compare_time_creation(file1: Path, file2: Path) -> Path:
            if self._date_filtering_method(
                file1.stat().st_ctime, file2.stat().st_ctime
            ):
                return file1
            return file2

        for list_duplicates in dublicates:
            not_delete_file = reduce(compare_time_creation, list_duplicates)
            logger.debug(
                f"File not delete: {not_delete_file}, \n time {not_delete_file.stat().st_ctime}"
            )
            for duplicate in list_duplicates:
                if duplicate != not_delete_file:
                    logger.debug(
                        f"Delete file: {duplicate}, \n time {duplicate.stat().st_ctime}"
                    )
                    yield duplicate
