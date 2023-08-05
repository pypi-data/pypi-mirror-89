"""Error container classes."""
from __future__ import annotations

from pathlib import PurePath
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Flake8Error(object):
    """A single error found in a module."""

    code: str = None
    """The flake8 or plugin error code"""
    message: str = None
    """The text of the error line"""
    row: int = None
    """The row of the error in the file"""
    column: int = None
    """The column of the error in the file"""
    line_text: str = None
    """The physical_line of the error"""
    module: Flake8ErrorModule = None
    """The Flake8ErrorModule parent container. Set in __init__ of Flake8ErrorModule"""

    @property
    def to_json(self) -> dict:
        """Convert self to dict."""
        return dict(code=self.code, message=self.message, row=self.row, column=self.column,
                    line_text=self.line_text, module=self.module.path)


@dataclass
class Flake8ErrorModule(object):
    """Wraps a flake8 error.

    One instance of this represents a single module.
    """

    path: str
    """The path of the filename."""

    errors: Union[List[Flake8Error], None] = None
    """The list of errors found in this module"""

    def __post_init__(self):
        """For setting self to each of the Flake8Error objects."""
        if self.errors:
            self.update_errors_parent()

        else:
            self.errors = []

    def update_errors_parent(self):
        """For setting self to each of the Flake8Error objects."""
        for err in self.errors:
            err.module = self

    @property
    def to_dict(self) -> dict:
        """Convert self to dict."""
        return {'path': self.path, 'errors': [e.to_json for e in self.errors]}

    @property
    def file_name_only(self) -> str:
        """Return the filename only.

        :return:
        """
        return PurePath(self.path).name

    @property
    def root_path_only(self) -> str:
        """Return only the path, excluding the module filename.

        :return:
        """
        return str(PurePath(self.path).parent)

    def short_path(self, max_parts: int = None, max_len: int = None, dots: bool = False) -> str:
        """Returns a shortened path string.

        :param max_parts: Max path parts to include
        :param max_len: Max string length
        :param dots: If the path is truncated, prefix with "..."
        :return:
        """
        if not any([max_len, max_parts]):
            return self.path

        pp = PurePath(self.path)

        if max_parts:
            pp = PurePath(*pp.parts[-max_parts:])

        if max_len:
            _max = max_len - 3 if dots else max_len
            value = str(pp)
            pp_str = '{}{}'.format('...' if dots and len(value) > max_len else '',
                                   value[-_max:])

            return pp_str

        return str(pp)

    def fit_path(self, max_len: int) -> str:
        """Truncate path to fit within max_len with "/~/" inserted.

        This removes path parts after the first to fit.

        The returned path is the first path part and the last parts that fit within
        the `max_len` value.

        :param max_len:
        :return:
        """
        if len(self.path) <= max_len:
            return self.path

        pp = PurePath(self.path)
        parts = pp.parts

        # Start with the overall length less the first path part + 3
        width = (len(self.path) + 3)
        start = 1

        for part in parts[1:]:
            start += 1
            width -= len(part)

            if width <= max_len:
                break

        out_pp = PurePath(*[parts[0]] + ['~'] + list(parts[start:]))

        return str(out_pp)

    def matches_prefixes(self, prefixes: List[str]) -> bool:
        """Check to see if our path matches any of the prefixes filters.

        The prefixes are (for now) simple strings.

        :param prefixes
        :return: True if any matches are found
        """
        flags = [self.path.startswith(p) for p in prefixes]

        return any(flags)
