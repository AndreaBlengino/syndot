from syndot.parser.parser import command_parser, CommandFormatter


list_parser = command_parser.add_parser(
    'list',
    prog="syndot list",
    usage="%(prog)s [-d | --directory] [[-l | --label] | [-p | --path]] | "
          "[[-s | --search] <SEARCH>] [[-m | --mapfile] <MAP_FILE>]",
    description="List dotfiles in the map file",
    help="List dotfiles in the map file",
    add_help=False,
    formatter_class=CommandFormatter
)

list_targets = list_parser.add_mutually_exclusive_group(required=False)

list_parser.add_argument(
    '-d', '--directory',
    action='store_true',
    default=False,
    required=False,
    dest='directory',
    help="Print the settings directory"
)

list_targets.add_argument(
    '-l', '--label',
    action='store_true',
    default=False,
    required=False,
    dest='label',
    help="List only target labels. Not allowed together with the "
         "[-p | --path] or [-s | --search] options"
)

list_targets.add_argument(
    '-p', '--path',
    action='store_true',
    default=False,
    required=False,
    dest='path',
    help="List only target paths. Now allowed together with the "
         "[-l | --label] or [-s | --search] options"
)

list_targets.add_argument(
    '-s', '--search',
    required=False,
    dest='search',
    metavar='<SEARCH>',
    help="List paths of the specified <SEARCH> label. Not allowed together "
         "with the [-l | --label] or [-p | --path] options"
)
