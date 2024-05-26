from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


unlink_parser = command_parser.add_parser('unlink',
                                          prog = 'syndot unlink',
                                          usage = '%(prog)s [OPTION] [ARGUMENT]',
                                          description = 'Remove symlinks and move dotfiles from <SETTINGS> directory '
                                                        'to their original directories',
                                          help = 'Remove symlinks and move dotfiles from <SETTINGS> directory to their '
                                                 'original directories',
                                          add_help = False,
                                          formatter_class = CommandFormatter)
unlink_parser._positionals.title = 'ARGUMENTS'
unlink_parser._optionals.title = 'OPTIONS'
unlink_targets = unlink_parser.add_mutually_exclusive_group(required = True)
unlink_targets.add_argument('TARGET_PATH_START',
                            nargs = '?',
                            metavar = 'TARGET_PATH',
                            help = 'Dotfile path, mandatory if [-a | -all] is not provided')
unlink_targets.add_argument('-a', '--all',
                            action = 'store_true',
                            default = False,
                            required = False,
                            dest = 'all',
                            help = 'Select all dotfiles in the <MAP_FILE>, mandatory if <TARGET_PATH> is not provided')
unlink_parser.add_argument('-e', '--exact',
                           action = 'store_true',
                           default = False,
                           required = False,
                           dest = 'exact',
                           help = 'Search for an exact match for the <TARGET_PATH> in the map file. If not provided, '
                                  'search for all targets which paths begin with <TARGET_PATH> in the map file')
unlink_parser.add_argument('-h', '--help',
                           action = 'help',
                           default = SUPPRESS,
                           help = 'Show this help message and exit')
unlink_parser.add_argument('-m', '--mapfile',
                           required = False,
                           metavar = '<MAP_FILE>',
                           help = 'Path to the %(metavar)s. If not provided search for a \'map.ini\' file in the '
                                  'current directory, so not required if current directory is the <SETTINGS> directory')
