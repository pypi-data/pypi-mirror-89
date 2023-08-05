
# D100 - No public module docstring
# To generate errors: flake8 gitlab_flake8_issues/nightmare
# D104 - no docstring in __init__.py
from __future__ import annotations
# F401 - unused and multiple/line
import sys, os
from typing import overload
# Generate F403
from collections import *

__all__ = ('OldStyle', 'not_found_symbol')  # F822

# max-complexity = 5
# max-line-length = 90
# max-doc-length = 80


def _bad_imports():
    # This will crash pydocstyle.parser
    # from datetime import *
    pass


def no_docstring_E302():
    unused = 'F841: Not used variable'


def blank_line_after_doc():
    """To generate D202.

    """
    pass


def not_imperative():
    """This will generate D401."""
    pass


def no_period():
    """Generate D400 no ending period"""
    pass


def blank_line_after_doc_before_code():
    """Generate D202."""

    return "chocolate"
def no_blank_lines_before():
    """Generate E302 error."""
    pass


def wrong_oneliner():
    """Generate a D200.

    """
    pass


def no_blank_after_summary():
    """Generate a D205.
    Should be space above this line.
    """
    pass


def escape_in_docstring():
    """Gen D301.

    \tComment - D301

     D207
    """
    pass


def docstring_over_indented():
        """Generate D208."""
        return "E117 - over indented"


def over_indented_docstring():
    """
        Generate D207.

        This is bad.
    """
    pass


def under_indented():
    """Generate D207.

    Not sure how to generate "D207": "Docstring is under-indented".

    """
    # TODO: Research how to create a D207 warning
    pass


def quotes_on_same_line_for_multi():
    """generate D209 and D403.

    This will trigger!"""
    pass


def white_space_bad():
    """Generate D210. """
    pass


def section():  # noqa: D416
    """Check section.

    returns
    -------
    Text within the section.

    """
    pass


def triple_double_quotes():
    '''Generate D300.'''
    pass


def this_should_not_start_with_this():
    """This will generate D404.

    (But it doesn't - 401 instead).
    """
    pass


def no_argument_desc(one, two):
    """Generate D417.

    Except it doesn't.

    :return:
    """
    return one, two


def continue_under_indented(one, two):
    """Get E128 error."""
    print('This is under indented: {} {}'.format(one,
                                                two))

    print('This should generate E502 ' + \
        'error')

    # Generate E124
    no_argument_desc(one='1',
                     two='2'
                    )


# Should generate E127
val = no_argument_desc(one='1',
                                two='2')


# Generate E203, E231
val_1, val_2 = no_argument_desc(1 ,2)


def no_space_operators():
    """Get E225."""
    return 1+ 2


# Generate E241
def too_many_spaces(one,    two):
    """Get E241 (but it doesn't)."""
    print('{}{}'.format(one,  two))#Generate E261, E262
    #Generate E265


# Generate E711
none = None
if none == None:
    print('is none')


def bare_except():
    """Generate E722."""
    try:
        no_space_operators()
    except:
        pass


# Generate E731
ll = lambda x: x + 1


# Generate E741
O = 1000


# Generate F402
def _shadowed():
    for sys in range(0, 10):
        print(sys)


# Generate F509
print('%z' % "F509")
# Generate F524, F522
print('{one}{two}'.format(one='1', three='3'))
# Generate F523
print('{}'.format('1', '2'))


# Generate F601
table = {
    'one': '1',
    'two': '2',
    'one': 'another 1',
}

# Crashes pydocstring
# cat, *dog, *bird = 1, 2, 3

# Generate F632
result = "abc" is not "abc"


# Generate F405
print(name)
name = 'hello'


# This will crash pydocstring
# def _duplicate_name(name, name):
#     print(name)

# Raise F901
def _wrong_not_implemented():
    raise NotImplemented()


# Raise W291 (PyCharm will auto-strip - must be on this line when saving)
var = "hello"

# Generate W605
invalid_escape = "\*"


def too_complex_function(value: str):
    """Generate C901."""
    if value == 'a':
        return 100

    for outer in range(0, 10):
        for inner in range(0, outer):
            if inner == 10:
                return outer

            if outer == inner:
                return inner

            if inner == 0:
                if outer == 0:
                    return 100

    for x in range(0, 10):
        if outer == 10:
            return "something"

    # F821
    if "value" == undefined_variable:
        return (0, 1, 2)


def blank_line_before_docstring():

    """Remove blank lines before docstring (D201)"""


too_long_line = "-------------------------------------------------------------------"
"""E501"""


def docstring_too_long():
    """Get a W505 error.

    This line will generate a E501 and.......................................................W505 error.
    """
    pass


class OldStyle:  # D101
    def __init__(self):  # D107
        pass


    def foo(self):  # D103 no docstring, E303 too many blank lines
        return "bar"

    def __str__(self):  # D105 Missing docstring in magic method
        return "old_style"

    class Nested(object):  # D106
        pass


class NewStyle(object):

    """For D211 - blank line before docstring."""


# E402, F401, W292 Don't put a space after this line
from collections import namedtuple