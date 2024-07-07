from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


rename_parser = command_parser.add_parser(
    'rename',
    prog="syndot rename",
    usage="%(prog)s ([-o | --old] <OLD_LABEL>) ([-n | --new] <NEW_LABEL>) "
          "[[-m | --mapfile] <MAP_FILE>]",
    description="Rename existing label in the map file",
    help="Rename existing label in the map file",
    add_help=False,
    formatter_class=CommandFormatter)

rename_parser.add_argument(
    '-h', '--help',
    action='help',
    default=SUPPRESS,
    help="Show this help message and exit")

rename_parser.add_argument(
    '-m', '--mapfile',
    required=False,
    metavar='<MAP_FILE>',
    help="Path to the %(metavar)s. If not provided search for a 'map.ini' "
         "file in the current directory, so not required if the current "
         "directory is the settings directory")

rename_parser.add_argument(
    '-n', '--new',
    required=True,
    dest='new_label',
    metavar='<NEW_LABEL>',
    help="New label to use")

rename_parser.add_argument(
    '-o', '--old',
    required=True,
    dest='old_label',
    metavar='<OLD_LABEL>',
    help="Existing label to rename")
