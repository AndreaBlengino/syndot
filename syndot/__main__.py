from syndot import commands
from syndot.parser.parser import parser
from syndot.parser.remove_parser import remove_parser
from syndot import init_config


init_config.init_config()
command_map = {
    'init': commands.init.init,
    'link': commands.link.link,
    'unlink': commands.unlink.unlink,
    'diffuse': commands.diffuse.diffuse,
    'add': commands.add.add,
    'remove': commands.remove.remove,
    'rename': commands.rename.rename,
    'list': commands.list_.list_
}


def main():
    args = parser.parse_args()

    if args.command == 'remove' and args.label is None and args.path is None:
        remove_parser.error(
            "At least a [-l | --label] or a [-p | --path] must be specified"
        )

    command_map[args.command](args=args)


if __name__ == "__main__":
    main()
