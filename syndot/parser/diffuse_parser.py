from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


diffuse_parser = command_parser.add_parser(
    'diffuse',
    prog='syndot diffuse',
    usage='%(prog)s ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) '
          '[[-m | --mapfile] <MAP_FILE>] [[-s | --start] <PATH_START>]',
    description='Create dotfiles symlinks',
    help='Create dotfiles symlinks',
    add_help=False,
    formatter_class=CommandFormatter)

diffuse_parser.add_argument(
    '-h', '--help',
    action='help',
    default=SUPPRESS,
    help='Show this help message and exit')

diffuse_parser.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar='<LABEL>',
    help='Label(s) to diffuse the associated path(s). At least a <LABEL> or a '
         '<PATH> must be provided')

diffuse_parser.add_argument(
    '-m', '--mapfile',
    required=False,
    metavar='<MAP_FILE>',
    help='Path to the %(metavar)s. If not provided search for a \'map.ini\' '
         'file in the current directory, so not required if the current '
         'directory is the settings directory')

diffuse_parser.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help='Dotfile path(s) to diffuse. At least a <LABEL> or a <PATH> must '
         'be provided')

diffuse_parser.add_argument(
    '-s', '--start',
    required=False,
    dest='start',
    metavar='<PATH_START>',
    help='Filter target based on path starting with <PATH_START>')
