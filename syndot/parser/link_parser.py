from syndot.parser.parser import command_parser, CommandFormatter


link_parser = command_parser.add_parser(
    'link',
    prog="syndot link",
    usage="%(prog)s [-b | --backup] ([-i | --interactive] | "
          "[[-l | --label] <LABEL>...] | [[-p | --path] <PATH>...]) "
          "[[-m | --mapfile] <MAP_FILE>] [-n | --no-confirm] "
          "[[-s | --start] <PATH_START>] ",
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

targets_group = link_parser.add_mutually_exclusive_group(required=False)

targets_group.add_argument(
    '-i', '--interactive',
    action='store_true',
    default=False,
    required=False,
    dest='interactive',
    help="Select label(s) to link the associated path(s) in interactive mode "
         "using gum. At least a label must be selected. Not allowed together "
         "with [-l | --label] or [-p | --path] options"
)

targets_group.add_argument(
    '-l', '--label',
    required=False,
    nargs='+',
    dest='label',
    metavar="<LABEL>",
    help="Label(s) to link the associated path(s). At least a <LABEL> must be "
         "provided. Not allowed together with [-i | --interactive] or "
         "[-p | --path] options"
)

targets_group.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to link. At least a <PATH> must be provided. Not "
         "allowed together with [-i | --interactive] or [-l | --label] options"
)
