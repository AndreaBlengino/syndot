from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


add_parser = command_parser.add_parser(
    'add',
    prog="syndot add",
    usage="%(prog)s ([-l | --label] <LABEL>) ([-p | --path] <PATH>...) "
          "[[-m | --mapfile] <MAP_FILE>]",
    description="Add dotfiles to the map file",
    help="Add dotfiles to the map file",
    add_help=False,
    formatter_class=CommandFormatter)

add_parser.add_argument(
    '-h', '--help',
    action='help',
    default=SUPPRESS,
    help="Show this help message and exit")

add_parser.add_argument(
    '-l', '--label',
    required=True,
    dest='label',
    metavar='<LABEL>',
    help="Label under which to group multiple target paths relating to "
         "the same set of configurations. A single label must be provided")

add_parser.add_argument(
    '-m', '--mapfile',
    required=False,
    metavar='<MAP_FILE>',
    help="Path to the %(metavar)s. If not provided search for a 'map.ini' "
         "file in the current directory, so not required if the current "
         "directory is the settings directory")

add_parser.add_argument(
    '-p', '--path',
    required=True,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to be added to the map file and grouped under "
         "<LABEL>. At least a path must be provided")
