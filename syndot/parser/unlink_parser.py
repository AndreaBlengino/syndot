from syndot.parser.parser import command_parser, CommandFormatter


unlink_parser = command_parser.add_parser(
    'unlink',
    prog="syndot unlink",
    usage="%(prog)s ([-i | --interactive] | [[-l | --label] <LABEL>...] | "
          "[[-p | --path] <PATH>...]) [[-m | --mapfile] <MAP_FILE>] "
          "[-n | --no-confirm] [[-s | --start] <PATH_START>]",
    description="Remove symlinks and move dotfiles from settings directory "
                "to their original directories",
    help="Remove symlinks and move dotfiles from settings directory to "
         "their original directories",
    add_help=False,
    formatter_class=CommandFormatter
)

targets_group = unlink_parser.add_mutually_exclusive_group(required=False)

targets_group.add_argument(
    '-i', '--interactive',
    action='store_true',
    default=False,
    required=False,
    dest='interactive',
    help="Select label(s) to unlink the associated path(s) in interactive "
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
    help="Label(s) to unlink the associated path(s). At least a <LABEL> must "
         "be provided. Not allowed together with [-i | --interactive] or "
         "[-p | --path] options"
)

targets_group.add_argument(
    '-p', '--path',
    required=False,
    nargs='+',
    dest='path',
    metavar='<PATH>',
    help="Dotfile path(s) to unlink. At least a <PATH> must be provided. Not "
         "allowed together with [-i | --interactive] or [-l | --label] options"
)
