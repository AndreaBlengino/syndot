__all__ = [
    "add_parser",
    "diffuse_parser",
    "init_parser",
    "link_parser",
    "list_parser",
    "remove_parser",
    "rename_parser",
    "unlink_parser",
]

from argparse import SUPPRESS
from syndot.parser.add_parser import add_parser
from syndot.parser.diffuse_parser import diffuse_parser
from syndot.parser.init_parser import init_parser
from syndot.parser.link_parser import link_parser
from syndot.parser.list_parser import list_parser
from syndot.parser.remove_parser import remove_parser
from syndot.parser.rename_parser import rename_parser
from syndot.parser.unlink_parser import unlink_parser

help_option_parsers = [
    add_parser,
    diffuse_parser,
    init_parser,
    link_parser,
    list_parser,
    remove_parser,
    rename_parser,
    unlink_parser
]

map_option_parsers = [
    add_parser,
    diffuse_parser,
    link_parser,
    list_parser,
    remove_parser,
    rename_parser,
    unlink_parser
]

start_option_parsers = [
    diffuse_parser,
    link_parser,
    unlink_parser
]

confirmation_option_parsers = [
    diffuse_parser,
    link_parser,
    unlink_parser
]

for parser in [
    add_parser,
    diffuse_parser,
    init_parser,
    link_parser,
    list_parser,
    remove_parser,
    rename_parser,
    unlink_parser
]:
    if parser in help_option_parsers:
        parser.add_argument(
            '-h', '--help',
            action='help',
            default=SUPPRESS,
            help="Show this help message and exit"
        )

    if parser in map_option_parsers:
        parser.add_argument(
            '-m', '--mapfile',
            required=False,
            metavar='<MAP_FILE>',
            help="Path to the %(metavar)s. If not provided search for a "
                 "'map.ini' file in the current directory, so not required if "
                 "the current directory is the settings directory"
        )

    if parser in start_option_parsers:
        parser.add_argument(
            '-s', '--start',
            required=False,
            dest='start',
            metavar='<PATH_START>',
            help="Filter target based on path starting with <PATH_START>"
        )

    if parser in confirmation_option_parsers:
        parser.add_argument(
            '-n', '--no-confirm',
            action='store_true',
            default=False,
            required=False,
            dest='no_confirm',
            help="Do not ask for confirmation"
        )
