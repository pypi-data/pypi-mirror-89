"""Reporters registered with flake8.

Sadly, I did not find a plugin just for flake8 to do this. There is a nice
plug-in for pytest:

See: https://github.com/numirias/pytest-json-report

"""
import atexit
from typing import Dict

from flake8.formatting import base
# noinspection PyProtectedMember
from flake8.options.manager import OptionManager
from flake8.style_guide import Violation
from flake8_report.flake8_error import Flake8Error, Flake8ErrorModule
import flake8_report.version as version

errors: Dict[str, Flake8ErrorModule] = {}
"""Accumulator for error/modules. Key: filename/path, data: Flake8ErrorModule"""


class BaseReporter(base.BaseFormatter):
    """Registered formatter for flake8."""

    name = 'flake8-report'
    version = version.__version__

    def __init__(self, options, output_type: str = None):
        super().__init__(options)

        self.options = options
        """Command-line and config options"""

        self.output_type: str = output_type

        # NOTE(bredbeddle): We will not receive the verbose option
        if options.verbose:
            options_dict = vars(options)
            for option in sorted(options_dict.keys()):
                print('{}: {}'.format(option, options_dict[option]))

        # Register the function called to generate the report on exit
        atexit.register(on_exit_report_print,
                        listing_type=self.output_type,
                        grouping=options.report_group,
                        style=options.report_style,
                        verbose=options.verbose)

    @classmethod
    def add_options(cls, mgr: OptionManager):
        """Add config options."""
        from argparse import ArgumentError

        try:
            mgr.add_option(
                '--report-style', choices=['none', 'group'],
                default='none', parse_from_config=True,
                help='Report style (Default: %(default)s)',
            )

            mgr.add_option(
                '--report-group', choices=['none', 'code', 'path'],
                default='none', parse_from_config=True,
                help='Report error grouping (Default: %(default)s)',
            )

        except ArgumentError:
            pass

    def handle(self, error: Violation):
        """Handle error from flake8."""
        f8_module = errors.get(error.filename)
        if not f8_module:
            f8_module = Flake8ErrorModule(path=error.filename)
            errors[error.filename] = f8_module

        f8_error = Flake8Error(code=error.code,
                               message=error.text,
                               row=error.line_number,
                               column=error.column_number,
                               line_text=error.physical_line,
                               module=f8_module)

        f8_module.errors.append(f8_error)

    def format(self, error: Violation):
        """Overload to do nothing."""
        pass

    def finished(self, filename):
        """Called when the module is done."""
        if self.options.verbose:
            print('Done with module. {} Errors found'.format(len(errors)))


class Flake8Report(BaseReporter):
    """Generate a report from error violations.

    This is used for `flake8 --format report`

    """

    def __init__(self, options):
        super().__init__(options, output_type='report')


class Flake8Checklist(BaseReporter):
    """Generate a checklist listing from error violations.

    This is used for `flake8 --format checklist`

    """

    def __init__(self, options):
        super().__init__(options, output_type='checklist')


def on_exit_report_print(listing_type: str, grouping: str = 'none', style: str = 'none', verbose: bool = False):
    """Invoked when the process is exiting.

    We need to do this because the flake8 API for report plug-ins doesn't really have
    an overall on_complete().

    :param listing_type: One of report, checklist, wiki
    :param grouping: One of none, code, path
    :param style: One of none, group
    :param verbose:
    :return:
    """
    from flake8_report.formatters import handle_output_gen

    handle_output_gen(generate=listing_type, errors=errors, group=grouping, verbose=verbose)
