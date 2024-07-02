from syndot import commands
from syndot.parser.parser import parser
from syndot.parser.remove_parser import remove_parser
from syndot import init_config


init_config.init_config()
args = parser.parse_args()

if args.command == 'remove' and args.label is None and args.path is None:
    remove_parser.error("At least a [-l | --label] or a [-p | --path] must be"
                        "specified")

command_map = {'init': commands.init,
               'link': commands.link,
               'unlink': commands.unlink,
               'diffuse': commands.diffuse,
               'add': commands.add,
               'remove': commands.remove,
               'list': commands.list_}

command_map[args.command](args=args)
