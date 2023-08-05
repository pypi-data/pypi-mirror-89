"""Formatters."""

from __future__ import annotations

from datetime import datetime
from typing import Callable, IO, Union, Set, Dict
import sys

from flake8_report.flake8_error import Flake8ErrorModule
from flake8_report.formatters.group_by import Grouping


def handle_output_gen(generate: str,
                      errors: Dict[str, Flake8ErrorModule],
                      group: Union[str, None] = None,
                      style: Union[str, None] = None,
                      verbose: bool = False):
    """Called when flake8 is done to generate our formatted report/listings.

    :param generate:
    :param errors:
    :param group: Type of grouping. One of [path, code]
    :param style: Style of output. One of [None, group]
    :param verbose: If True, output detailed messages
    :return:
    """
    from flake8_report.formatters.report import ReportGenerator
    from flake8_report.formatters.group_by import GroupBy
    from flake8_report.formatters.sorters import Sorter

    # Do nothing if there is nothing to do.
    if not errors:
        print('No errors found - congratulations!')
        return

    if verbose:
        print('Report format: {}'.format(generate))
        print('Group-by     : {}'.format(group))

    # Create the GroupBy (which might be ungrouped)
    err_group = GroupBy.create_instance(group_type=group)

    # Create the output generator
    generator = OutputGenerator.create_instance(output_type=generate)
    generator.add_feature(ReportGenerator.SHOW_TEXT)

    # Create the error groups
    flat_err_list = Sorter.flatten(err_modules=list(errors.values()))
    error_grps = err_group.group(errors=flat_err_list)

    generator.generate(error_groups=error_grps)


def save_errors_as_json(errors: Dict[Flake8ErrorModule], filename: str = "flake8.json") -> None:
    """Save the errors content to a JSON file.

    :param errors: List of Flake8ErrorModule items to save
    :param filename: Name of file to write to
    :return:
    """
    import json

    with open(filename, 'w+') as fp:
        dd = {}
        for mod in errors.values():
            print('{}: Count of errors: {}'.format(mod.path, len(mod.errors)))
            dd[mod.path] = mod.to_dict

        json.dump(dd, fp, indent=4)


class OutputGenerator(object):
    """Base class for report output generators.

    Reports need to implement the :py:method:`report_logic` method.

    """

    SHOW_TEXT = 1
    SHOW_ROW_COL = 2
    SHOW_MODULE = 3
    SHOW_HEADER = 4
    SHOW_SUMMARY = 5

    H1 = '# '
    H2 = '## '
    H3 = '### '
    H4 = '#### '

    std_date_fmt = '{:%Y-%m-%d %H:%M %a}'

    def __init__(self, features: Set[int] = None, write_to: Union[Callable, IO] = sys.stdout):
        """Initialize.

        :param features: A set with the SHOW_* flags to enable features
        :param write_to: Either a file-like object or a callable
        """
        self.write_to = write_to

        self.show_text = self.SHOW_TEXT in features
        """Show the code lines for the error"""
        self.show_row_col = self.SHOW_ROW_COL in features
        """Show the row:column"""
        self.show_module = self.SHOW_MODULE in features
        """Show the module name"""
        self.show_header = self.SHOW_HEADER in features
        """Show the report header"""
        self.show_summary = self.SHOW_SUMMARY in features
        """Show the report summary"""

        self.features: Set = features
        self.dt_generated: datetime = datetime.now()

    def add_feature(self, feature: int):
        """Add a report feature."""
        self.features.add(feature)

    @classmethod
    def create_instance(cls, output_type: Union[str, None], features: Set = None) -> OutputGenerator:
        """Create an output generator instance.

        If `report_type` is None this defaults to "report".

        :param output_type: One of [report, checklist, None]
        :param features: Optional set of features to enable for the output generator
        :return: An OutputGenerator instance
        """
        from .report import ReportGenerator
        from .checklist import ChecklistGenerator
        from .wiki import WikiGenerator

        report = {
            'none': ReportGenerator,
            None: ReportGenerator,
            'report': ReportGenerator,
            'checklist': ChecklistGenerator,
            'wiki': WikiGenerator
        }[output_type]

        return report(features=features)

    def generate(self, error_groups: Grouping, verbose: bool = False):
        """Generate the formatted output.

        :param error_groups: The container of Groups with Flake8Error items
        :param verbose: If True, print detail messages
        :return:
        """
        raise NotImplementedError()

    def render_line(self, line: str) -> None:
        """Print the output line to the target.

        This will write to :py:attribute:`write_to`:

        * If it is a callable, the signature must accept a single string parameter
        * If it is not callable it is presumed to be a file-type object
          (i.e., sys.stdout or open file)

        :param line: Line to print
        :return:
        """
        if hasattr(self.write_to, '__call__'):
            self.write_to(line)
        else:
            print(line, file=self.write_to)

    def render_checkbox_line(self, line: str, level: int = 0) -> None:
        """Print a list line item with proper level indenting.

        :param line:
        :param level:
        :return:
        """
        tag = '- [ ]'
        indent = ' ' * (2 * level)

        content = '{indent}{tag} {msg}'.format(indent=indent, tag=tag, msg=line)
        self.render_line(line=content)

    def render_header_line(self, line: str, level: str = H1) -> None:
        """Print a header line at a specified level.

        This will always print a newline before/after the header...because markdown.

        For example, if level is set to H2:

        .. sourcecode: text

            "## The text of the line"

        :param line: Text line to render
        :param level: The level for the header
        :return:
        """
        self.render_line('\n{}{}\n'.format(level, line))

    def render_blank_line(self, cnt: int = 1) -> None:
        """Render a blank line"""
        for _ in range(0, cnt):
            self.render_line('')

    def get_report_time(self, dt: datetime = None) -> str:
        """Get our standard datetime formatted string."""
        return self.std_date_fmt.format(dt or self.dt_generated)

    def render_code_text(self, text: str) -> None:
        """Render the line_text with indent.

        The structure is:
        * Each line is indented 2 spaces
        * First line has a label "Text:"
        * Each subsequent line indented and prefixed with ":"

        :param text:
        :return:
        """
        if not text:
            return

        first = "  : "
        other = "  : "
        indent = first

        for line in [_line for _line in text.rstrip('\n').split('\n') if _line]:
            self.render_line('{}{}'.format(indent, line))
            indent = other
