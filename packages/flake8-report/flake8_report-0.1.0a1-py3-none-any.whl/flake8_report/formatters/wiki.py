"""For generating Gitlab checklists."""
from __future__ import annotations

import sys
from typing import Set, Union, Callable
from typing.io import IO
from flake8_report.formatters import OutputGenerator
from flake8_report.formatters.group_by import Grouping


class WikiGenerator(OutputGenerator):
    """Generate a wiki markdown for pasting into a Gitlab wiki page."""

    def __init__(self, features: Set[int] = None, write_to: Union[Callable, IO] = sys.stdout):
        if not features:
            features = {self.SHOW_ROW_COL, self.SHOW_MODULE}
        super().__init__(features=features, write_to=write_to)

        self.features: Set = features

    def add_feature(self, feature: int):
        """Add a report feature."""
        self.features.add(feature)

    def generate(self, error_groups: Grouping, verbose: bool = False):
        """Generate ungrouped report listing.

        This expects the `error_groups` to have only a single group it in. If
        we happen to have > 1, this will instead invoke :py:class:`GroupReportGenerator`.

        :param error_groups:
        :param verbose:
        :return:
        """
        pass
