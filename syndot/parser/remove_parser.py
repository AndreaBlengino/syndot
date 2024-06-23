from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


remove_parser = command_parser.add_parser('remove',
                                          prog='syndot remove',
                                          usage='%(prog)s [OPTION] ARGUMENT',
                                          description='Remove dotfiles from the map file',
                                          help='Remove dotfiles from the map file',
                                          add_help=False,
                                          formatter_class=CommandFormatter)
remove_parser._positionals.title = 'ARGUMENTS'
remove_parser._optionals.title = 'OPTIONS'
remove_parser.add_argument('TARGET_PATH',
                           help='Dotfile path')
remove_parser.add_argument('-h', '--help',
                           action='help',
                           default=SUPPRESS,
                           help='Show this help message and exit')
remove_parser.add_argument('-m', '--mapfile',
                           required=False,
                           metavar='<MAP_FILE>',
                           help='Path to the %(metavar)s. If not provided search for a \'map.ini\' file in the '
                                'current directory, so not required if current directory is the <SETTINGS> directory')
