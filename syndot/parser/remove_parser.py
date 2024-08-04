from syndot.parser.parser import command_parser, CommandFormatter


remove_parser = command_parser.add_parser(
    'remove',
    prog="syndot remove",
    usage="%(prog)s ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) "
          "[[-m | --mapfile] <MAP_FILE>]",
    description="Remove dotfiles from the map file",
    help="Remove dotfiles from the map file",
    add_help=False,
    formatter_class=CommandFormatter
)

remove_parser.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar='<LABEL>',
    help="Label(s) and relative path(s) to remove from the map file. One or "
         "more labels can be provided. At least a <LABEL> or a <PATH> must be "
         "provided"
)

remove_parser.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to remove from the map file. One of more paths can "
         "be provided. At least a <LABEL> or a <PATH> must be provided"
)
