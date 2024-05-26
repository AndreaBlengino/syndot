from syndot import commands
from syndot.parser.parser import parser
from syndot import init_config


init_config.init_config()
args = parser.parse_args()

command_map = {'init': commands.init,
               'link': commands.link,
               'unlink': commands.unlink,
               'diffuse': commands.diffuse,
               'add': commands.add,
               'remove': commands.remove,
               'list': commands.list_}

command_map[args.command](args = args)
