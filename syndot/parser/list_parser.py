from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


list_parser = command_parser.add_parser('list',
                                        prog = 'syndot list',
                                        usage = '%(prog)s [OPTION]',
                                        description = 'List dotfiles in the map file',
                                        help = 'List dotfiles in the map file',
                                        add_help = False,
                                        formatter_class = CommandFormatter)
list_parser._positionals.title = 'ARGUMENTS'
list_parser._optionals.title = 'OPTIONS'
list_parser.add_argument('-h', '--help',
                         action = 'help',
                         default = SUPPRESS,
                         help = 'Show this help message and exit')
list_parser.add_argument('-m', '--mapfile',
                         required = False,
                         metavar = '<MAP_FILE>',
                         help = 'Path to the %(metavar)s. If not provided search for a \'map.ini\' file in the '
                                'current directory, so not required if current directory is the <SETTINGS> directory')
