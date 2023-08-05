"""Sorter classes for sorting errors."""
from typing import List

from flake8_report.flake8_error import Flake8ErrorModule, Flake8Error


class Sorter(object):
    """The built-in error sorters."""

    @classmethod
    def sort(cls, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort by some key.

        :param errors: List of Flake8Error items.
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def flatten(cls, err_modules: List[Flake8ErrorModule]) -> List[Flake8Error]:
        """Flatten the list of error modules to list of Flake8Error items.

        :param err_modules:
        :return:
        """
        reply_list: List[Flake8Error] = []

        for err_mod in err_modules:
            reply_list.extend(err_mod.errors)
            # print('Added {} errors'.format(len(err_mod.errors)))

        # print('Returning from flatten: {} items'.format(len(reply_list)))
        return reply_list


class SortByCode(Sorter):
    """Sort the errors by the error code."""

    @classmethod
    def sort(cls, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort by error code."""
        sorted_list = sorted(errors, key=lambda x: x.code)

        return sorted_list


class SortByPath(Sorter):
    """Sort the errors by file module name."""

    @classmethod
    def sort(cls, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort by error module path name."""
        sorted_list = sorted(errors, key=lambda x: x.module.path)

        return sorted_list


class SortByUnsorted(Sorter):
    """Unsorted flattened list of errors."""

    @classmethod
    def sort(cls, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Return unsorted flattened list of errors."""
        return errors
