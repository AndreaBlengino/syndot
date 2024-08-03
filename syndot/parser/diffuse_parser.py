from syndot.parser.parser import command_parser, CommandFormatter


diffuse_parser = command_parser.add_parser(
    'diffuse',
    prog="syndot diffuse",
    usage="%(prog)s ([-i | --interactive] | [[-l | --label] <LABEL>...] | "
          "[[-p | --path] <PATH>...]) [[-m | --mapfile] <MAP_FILE>] "
          "[-n | --no-confirm] [[-s | --start] <PATH_START>]",
    description="Create dotfiles symlinks",
    help="Create dotfiles symlinks",
    add_help=False,
    formatter_class=CommandFormatter
)

targets_group = diffuse_parser.add_mutually_exclusive_group(required=False)

targets_group.add_argument(
    '-i', '--interactive',
    action='store_true',
    default=False,
    required=False,
    dest='interactive',
    help="Select label(s) to diffuse the associated path(s) in interactive "
         "mode using gum, if it is installed in the system. At least a label "
         "must be selected. Not allowed together with [-l | --label] or "
         "[-p | --path] options"
)

targets_group.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar='<LABEL>',
    help="Label(s) to diffuse the associated path(s). At least a <LABEL> must "
         "be provided. Not allowed together with [-i | --interactive] or "
         "[-p | --path] options"
)

targets_group.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to diffuse. At least a <PATH> must be provided. Not "
         "allowed together with [-i | --interactive] or [-l | --label] options"
)
