from syndot.parser.parser import command_parser, CommandFormatter


rename_parser = command_parser.add_parser(
    'rename',
    prog="syndot rename",
    usage="%(prog)s ([-o | --old] <OLD_LABEL>) ([-n | --new] <NEW_LABEL>) "
          "[[-m | --mapfile] <MAP_FILE>]",
    description="Rename existing label in the map file",
    help="Rename existing label in the map file",
    add_help=False,
    formatter_class=CommandFormatter
)

rename_parser.add_argument(
    '-n', '--new',
    required=True,
    dest='new_label',
    metavar='<NEW_LABEL>',
    help="New label to use"
)

rename_parser.add_argument(
    '-o', '--old',
    required=True,
    dest='old_label',
    metavar='<OLD_LABEL>',
    help="Existing label to rename"
)
