from syndot.parser.parser import command_parser, CommandFormatter


init_parser = command_parser.add_parser(
    'init',
    prog="syndot init",
    usage="%(prog)s [[-p | --path] <PATH>]",
    description="Initialize settings directory where store dotfiles",
    help="Initialize settings directory where store dotfiles",
    add_help=False,
    formatter_class=CommandFormatter
)

init_parser.add_argument(
    '-p', '--path',
    required=False,
    dest='path',
    metavar='<PATH>',
    help="Path to the settings directory. If not provided, it creates the "
         "settings directory at the default path: ~/Settings"
)
