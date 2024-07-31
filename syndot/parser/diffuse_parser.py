from syndot.parser.parser import command_parser, CommandFormatter


diffuse_parser = command_parser.add_parser(
    'diffuse',
    prog="syndot diffuse",
    usage="%(prog)s ([[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) "
          "[[-m | --mapfile] <MAP_FILE>] [[-s | --start] <PATH_START>] "
          "[-n | --no-confirm]",
    description="Create dotfiles symlinks",
    help="Create dotfiles symlinks",
    add_help=False,
    formatter_class=CommandFormatter
)

diffuse_parser.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar='<LABEL>',
    help="Label(s) to diffuse the associated path(s). At least a <LABEL> or a "
         "<PATH> must be provided"
)

diffuse_parser.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to diffuse. At least a <LABEL> or a <PATH> must "
         "be provided"
)
