from argparse import SUPPRESS
from syndot.parser.parser import command_parser, CommandFormatter


link_parser = command_parser.add_parser('link',
                                        prog = 'syndot link',
                                        usage = '%(prog)s [OPTION] [ARGUMENT]',
                                        description = 'Move dotfiles to <SETTINGS> directory and create symlinks to '
                                                      'them',
                                        help = 'Move dotfiles to <SETTINGS> directory and create symlinks to them',
                                        add_help = False,
                                        formatter_class = CommandFormatter)
link_parser._positionals.title = 'ARGUMENTS'
link_parser._optionals.title = 'OPTIONS'
link_targets = link_parser.add_mutually_exclusive_group(required = True)
link_targets.add_argument('TARGET_PATH_START',
                          nargs = '?',
                          metavar = 'TARGET_PATH',
                          help = 'Dotfile path, mandatory if [-a | -all] option is not provided')
link_targets.add_argument('-a', '--all',
                          action = 'store_true',
                          default = False,
                          required = False,
                          dest = 'all',
                          help = 'Select all dotfiles in the <MAP_FILE>, mandatory if <TARGET_PATH> argument is not '
                                 'provided')
link_parser.add_argument('-b', '--backup',
                         action = 'store_true',
                         default = False,
                         required = False,
                         dest = 'backup',
                         help = 'Create a backup copy of the original dotfile')
link_parser.add_argument('-e', '--exact',
                         action = 'store_true',
                         default = False,
                         required = False,
                         dest = 'exact',
                         help = 'Search for an exact match for the <TARGET_PATH> in the map file. If not provided, '
                                'search for all targets which paths begin with <TARGET_PATH> in the map file')
link_parser.add_argument('-h', '--help',
                         action = 'help',
                         default = SUPPRESS,
                         help = 'Show this help message and exit')
link_parser.add_argument('-m', '--mapfile',
                         required = False,
                         metavar = '<MAP_FILE>',
                         help = 'Path to the %(metavar)s. If not provided search for a \'map.ini\' file in the current '
                                'directory, so not required if current directory is the <SETTINGS> directory')
