"""Group errors by key."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union, Set

from flake8_report.flake8_error import Flake8Error
import flake8_report.formatters.sorters as sorters


@dataclass
class Group(object):
    """A group of error items."""

    key: str
    errors: List[Flake8Error]

    def codes(self) -> Set:
        """The set of codes found within this group"""
        return set([err.code for err in self.errors])


@dataclass
class Grouping(object):
    """A grouping of Group items."""

    label: str
    groups: List[Group]

    def __len__(self):
        return len(self.groups)

    def error_count(self) -> int:
        """The total number of errors contained within this grouping.

        :return:
        """
        if not self.groups:
            return 0
        return sum([len(err.errors) for err in self.groups])

    def codes(self) -> Set:
        """The set of codes found within this grouping"""
        g_codes = [group.codes() for group in self.groups]
        return set([code for codes in g_codes for code in codes])


class GroupBy(object):
    """Base class to group the errors by a key.

    Reports will drive their listings from a list of :py:class:`Group` items. For
    reports that are ungrouped they will receive a list with a single :py:class:`Ungrouped`
    item containing all the errors.

    The errors within a group are sorted by the :py:attribute:`grp_error_sorter` (which also
    might be unsorted).

    """

    SORT_KEY = 'key'
    SORT_GROUP_ERR_COUNT = 'group_count'
    SORT_UNSORTED = 'unsorted'

    def __init__(self, label: str,
                 group_sort_by: str = SORT_KEY,
                 item_sort_by: sorters.Sorter = sorters.SortByUnsorted):
        """.

        :param group_sort_by: Sort groups by key, count, or unsorted
        :param item_sort_by: Sorter for items within group
        """
        self.group_sort_by: str = group_sort_by
        self.grp_error_sorter: sorters.Sorter = item_sort_by

        self.label = label
        """The type of grouping"""

    @classmethod
    def create_instance(cls, group_type: Union[str, None]) -> GroupBy:
        """Factory to create the GroupBy instance by label.

        :param group_type: One of [path, code]
        :return: A GroupBy instance
        """
        return {
            'none': Ungrouped,
            None: Ungrouped,
            'path': GroupByPath,
            'code': GroupByCode
        }[group_type]()

    def group(self, errors: List[Flake8Error]) -> Grouping:
        """Group errors by a key.

        :param errors: List of errors sorted by the group-by key.
        """
        prev_key = None
        groups: List[Group] = []
        curr_group: Group = None

        sorted_errs = self.pre_sort_errors(errors=errors)

        for err in sorted_errs:
            if prev_key != self.get_key(error=err):

                if curr_group:
                    groups.append(curr_group)

                curr_group = Group(key=self.get_key(err), errors=[err])
                prev_key = self.get_key(error=err)

            else:
                curr_group.errors.append(err)

        groups.append(curr_group) if curr_group.errors else print('Discarding empty group')
        sorted_groups = self.sort_groups(groups=groups)
        self.sort_errors_in_groups(groups=sorted_groups)

        return Grouping(label=self.label, groups=sorted_groups)

    def pre_sort_errors(self, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort the errors before doing grouping.

        :param errors: List of errors
        """
        raise NotImplementedError()

    def get_key(self, error: Flake8Error) -> Union[str, int]:
        """Return the group key from the error"""
        raise NotImplementedError()

    def sort_groups(self, groups: List[Group]) -> List[Group]:
        """Sort the groups by the key.

        :param groups:
        :return:
        """
        if self.group_sort_by == self.SORT_KEY:
            sorted_groups = sorted(groups, key=lambda x: x.key)

        elif self.group_sort_by == self.SORT_GROUP_ERR_COUNT:
            sorted_groups = sorted(groups, key=lambda x: len(x.errors), reverse=True)

        elif self.group_sort_by == self.SORT_UNSORTED:
            sorted_groups = groups

        else:
            raise ValueError('Unsupported sort_by: {}'.format(self.group_sort_by))

        return sorted_groups

    def sort_errors_in_groups(self, groups: List[Group]) -> List[Group]:
        """Sort the errors within each group.

        :param groups:
        :return:
        """
        for group in groups:
            group.errors = self.grp_error_sorter.sort(errors=group.errors)

        return groups


class Ungrouped(GroupBy):
    """An ungrouped GroupBy."""

    def __init__(self, item_sort_by: sorters.Sorter = sorters.SortByUnsorted):
        super().__init__(label='', group_sort_by=GroupBy.SORT_UNSORTED, item_sort_by=item_sort_by)

    def pre_sort_errors(self, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort before performing grouping."""
        sorter = sorters.SortByUnsorted()
        return sorter.sort(errors=errors)

    def group(self, errors: List[Flake8Error], sort_by: str = GroupBy.SORT_UNSORTED) -> Grouping:
        """Group errors into a single Group."""
        un_group = [Group(key='all', errors=errors)]

        sorted_un_group = self.sort_groups(groups=un_group)

        return Grouping(label=self.label, groups=sorted_un_group)

    def get_key(self, error: Flake8Error) -> Union[str, int]:
        """Unused."""
        pass


class GroupByCode(GroupBy):
    """Group the errors by error code."""

    def __init__(self,
                 group_sort_by: str = GroupBy.SORT_KEY,
                 item_sort_by: sorters.Sorter = sorters.SortByUnsorted):
        super().__init__(label='code', group_sort_by=group_sort_by, item_sort_by=item_sort_by)

    def pre_sort_errors(self, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort before performing grouping."""
        return sorters.SortByCode().sort(errors=errors)

    def get_key(self, error: Flake8Error) -> Union[str, int]:
        """Get the error's code."""
        return error.code


class GroupByPath(GroupBy):
    """Group the errors by module path/filename."""

    def __init__(self,
                 group_sort_by: str = GroupBy.SORT_KEY,
                 item_sort_by: sorters.Sorter = sorters.SortByCode):
        super().__init__(label='path', group_sort_by=group_sort_by, item_sort_by=item_sort_by)

    def pre_sort_errors(self, errors: List[Flake8Error]) -> List[Flake8Error]:
        """Sort before performing grouping."""
        return sorters.SortByPath().sort(errors=errors)

    def get_key(self, error: Flake8Error) -> Union[str, int]:
        """Get the error's module path."""
        return error.module.path
