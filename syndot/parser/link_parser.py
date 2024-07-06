from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


link_parser = command_parser.add_parser(
    'link',
    prog='syndot link',
    usage='%(prog)s [-b | --backup] ([[-l | --label] <LABEL>...] | '
          '[[-p | --path] <PATH>...]) [[-m | --mapfile] <MAP_FILE>] '
          '[[-s | --start] <PATH_START>]',
    description='Move dotfiles to settings directory '
                'and create symlinks to them',
    help='Move dotfiles to settings directory and create symlinks to them',
    add_help=False,
    formatter_class=CommandFormatter)

link_parser.add_argument(
    '-b', '--backup',
    action='store_true',
    default=False,
    required=False,
    dest='backup',
    help='Create a backup copy of the original dotfile')

link_parser.add_argument(
    '-h', '--help',
    action='help',
    default=SUPPRESS,
    help='Show this help message and exit')

link_parser.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar='<LABEL>',
    help='Label(s) to link the associated path(s). At least a <LABEL> or a '
         '<PATH> must be provided')

link_parser.add_argument(
    '-m', '--mapfile',
    required=False,
    metavar='<MAP_FILE>',
    help='Path to the %(metavar)s. If not provided search for a \'map.ini\' '
         'file in the current directory, so not required if the current '
         'directory is the settings directory')

link_parser.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help='Dotfile path(s) to link. At least a <LABEL> or a <PATH> must be '
         'provided')

link_parser.add_argument(
    '-s', '--start',
    required=False,
    dest='start',
    metavar='<PATH_START>',
    help='Filter target based on path starting with <PATH_START>')
