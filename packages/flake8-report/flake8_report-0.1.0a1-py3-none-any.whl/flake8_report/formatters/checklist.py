"""For generating Gitlab checklists."""
from __future__ import annotations

import sys
from typing import Set, Union, Callable
from typing.io import IO

from flake8_report.flake8_error import Flake8Error
from flake8_report.formatters import OutputGenerator
from flake8_report.formatters.codes_lookup import lookup_code_title
from flake8_report.formatters.group_by import Grouping


class ChecklistGenerator(OutputGenerator):
    """Generate a Gitlab checklist in markdown for importing into Gitlab project issues.

    Sadly, Gitlab's markdown does not support a fixed width character set apart from
    code or code blocks. And, there is no way to embed checkboxes into markdown tables.

    This will wrap the body of a checkbox line in `...` to properly light up the columns
    of the listing.
    """

    MAX_MSG_LEN = 50
    MAX_PATH_LEN = 50

    CONTENT_FMT_CODE = '`'
    CONTENT_FMT_ITALIC = '_'

    def __init__(self, features: Set[int] = None, write_to: Union[Callable, IO] = sys.stdout):
        if not features:
            features = {self.SHOW_ROW_COL, self.SHOW_MODULE}
        super().__init__(features=features, write_to=write_to)

        self.features: Set = features

    def add_feature(self, feature: int):
        """Add a report feature."""
        self.features.add(feature)

    def generate(self, error_groups: Grouping, verbose: bool = False):
        """Generate ungrouped checklist listing.

        :param error_groups:
        :param verbose:
        :return:
        """
        generator = self

        if len(error_groups) > 1:
            generator = GroupedChecklistGenerator(features=self.features,
                                                  write_to=self.write_to)

        generator.render_checklist(error_groups=error_groups)

    def render_checklist(self, error_groups: Grouping):
        """Render simple, ungrouped checklist"""
        group = error_groups.groups[0]

        for err in group.errors:
            self.render_error_line_alt(err=err)

    def render_error_line(self, err: Flake8Error) -> None:
        """One way to format the line"""
        mod_name = err.module.short_path(max_len=self.MAX_PATH_LEN, dots=True)
        row_col = '{:<}:{:<}'.format(err.row, err.column if err.column < 99 else 1)

        line = '`{:6} {:4} {:{max_msg}}  {:{max_path}}`'.format(
            row_col,
            err.code,
            err.message[:self.MAX_MSG_LEN].title(),
            mod_name,
            max_msg=self.MAX_MSG_LEN,
            max_path=self.MAX_PATH_LEN
        )

        self.render_checkbox_line(line=line)

    def render_error_line_alt(self, err: Flake8Error) -> None:
        """An alternate way to format the line"""
        mod_name = err.module.fit_path(max_len=self.MAX_PATH_LEN)
        row_col = '{:<}:{:<}'.format(err.row, err.column)

        line = '`{:4} {:{max_msg}}` {:}:{:}'.format(
            err.code,
            err.message[:self.MAX_MSG_LEN].title(),
            mod_name,
            row_col,
            max_msg=self.MAX_MSG_LEN
        )

        self.render_checkbox_line(line=line)


class GroupedChecklistGenerator(ChecklistGenerator):
    """Generate grouped checklists."""

    def __init__(self, features: Set[int] = None, write_to: Union[Callable, IO] = sys.stdout):
        super().__init__(features=features, write_to=write_to)

    def generate(self, error_groups: Grouping, verbose: bool = False):
        """Generate grouped checklist listing."""
        self.render_checklist(error_groups=error_groups)

    def render_checklist(self, error_groups: Grouping):
        """Render checklist output."""
        for group in error_groups.groups:

            self._render_grp_title(key=group.key, group_label=error_groups.label)

            for err in group.errors:

                if error_groups.label == 'code':
                    self.render_error_line_alt(err=err)

                elif error_groups.label == 'path':
                    self.render_by_path_item(err=err)

    def _render_grp_title(self, key: str, group_label: str):
        """Render the title of the group"""
        if group_label == 'path':
            self.render_header_line(key)

        elif group_label == 'code':
            title = lookup_code_title(code=key, default="Code description text not found")

            self.render_header_line('{} - {}'.format(key, title))

    def render_by_path_item(self, err: Flake8Error) -> None:
        """Render the line to display when grouping by code."""
        row_col = '{:<}:{:<}'.format(err.row, err.column)

        self.render_checkbox_line('{} [{:7}] {}'.format(
            err.code,
            row_col,
            err.message
        ))
