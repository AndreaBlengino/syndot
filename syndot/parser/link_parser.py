from syndot.parser.parser import command_parser, CommandFormatter


link_parser = command_parser.add_parser(
    'link',
    prog="syndot link",
    usage="%(prog)s [-b | --backup] ([[-l | --label] <LABEL>...] | "
          "[[-p | --path] <PATH>...]) [[-m | --mapfile] <MAP_FILE>] "
          "[[-s | --start] <PATH_START>] [-n | --no-confirm]",
    description="Move dotfiles to settings directory "
                "and create symlinks to them",
    help="Move dotfiles to settings directory and create symlinks to them",
    add_help=False,
    formatter_class=CommandFormatter
)

link_parser.add_argument(
    '-b', '--backup',
    action='store_true',
    default=False,
    required=False,
    dest='backup',
    help="Create a backup copy of the original dotfile"
)

link_parser.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar="<LABEL>",
    help="Label(s) to link the associated path(s). At least a <LABEL> or a "
         "<PATH> must be provided"
)

link_parser.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to link. At least a <LABEL> or a <PATH> must be "
         "provided"
)
