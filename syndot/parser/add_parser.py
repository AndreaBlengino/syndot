from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


add_parser = command_parser.add_parser('add',
                                       prog = 'syndot add',
                                       usage = '%(prog)s [OPTION] ARGUMENT',
                                       description = 'Add dotfiles to the map file',
                                       help = 'Add dotfiles to the map file',
                                       add_help = False,
                                       formatter_class = CommandFormatter)
add_parser._positionals.title = 'ARGUMENTS'
add_parser._optionals.title = 'OPTIONS'
add_parser.add_argument('TARGET_PATH',
                        help = 'Dotfile path')
add_parser.add_argument('-h', '--help',
                        action = 'help',
                        default = SUPPRESS,
                        help = 'Show this help message and exit')
add_parser.add_argument('-m', '--mapfile',
                        required = False,
                        metavar = '<MAP_FILE>',
                        help = 'Path to the %(metavar)s. If not provided search for a \'map.ini\' file in the '
                               'current directory, so not required if current directory is the <SETTINGS> directory')
