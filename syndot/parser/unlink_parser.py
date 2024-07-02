from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


unlink_parser = command_parser.add_parser(
    'unlink',
    prog='syndot unlink',
    usage='%(prog)s ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) '
          '[[-m | --mapfile] <MAP_FILE>]',
    description='Remove symlinks and move dotfiles from settings directory '
                'to their original directories',
    help='Remove symlinks and move dotfiles from settings directory to '
         'their original directories',
    add_help=False,
    formatter_class=CommandFormatter)

unlink_parser.add_argument(
    '-h', '--help',
    action='help',
    default=SUPPRESS,
    help='Show this help message and exit')

unlink_parser.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar='<LABEL>',
    help='Label(s) to unlink the associated path(s). At least a <LABEL> or a '
         '<PATH> must be provided')

unlink_parser.add_argument(
    '-m', '--mapfile',
    required=False,
    metavar='<MAP_FILE>',
    help='Path to the %(metavar)s. If not provided search for a \'map.ini\' '
         'file in the current directory, so not required if the current '
         'directory is the settings directory')

unlink_parser.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help='Dotfile path(s) to unlink. At least a <LABEL> or a <PATH> must be '
         'provided')
