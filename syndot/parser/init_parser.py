from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


init_parser = command_parser.add_parser('init',
                                        prog='syndot init',
                                        usage='%(prog)s [OPTION]',
                                        description='Initialize <SETTINGS> directory where store dotfiles',
                                        help='Initialize <SETTINGS> directory where store dotfiles',
                                        add_help=False,
                                        formatter_class=CommandFormatter)
init_parser._positionals.title = 'ARGUMENTS'
init_parser._optionals.title = 'OPTIONS'
init_parser.add_argument('-h', '--help',
                         action='help',
                         default=SUPPRESS,
                         help='Show this help message and exit')
init_parser.add_argument('-p', '--path',
                         required=False,
                         help='Path to the <SETTINGS> directory. If not provided, create the <SETTINGS> directory at '
                              'the default path: ~/Settings')
