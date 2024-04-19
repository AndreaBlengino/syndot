from argparse import ArgumentParser


parser = ArgumentParser()
command_parser = parser.add_subparsers(dest = 'command')

init_parser = command_parser.add_parser('init')
init_parser.add_argument('-p', '--path', required = False)

link_parser = command_parser.add_parser('link')
link_parser.add_argument('-m', '--mapfile', required = False)
link_parser.add_argument('-b', '--backup', action = 'store_true', default = False, required = False)
link_parser.add_argument('-f', '--force', action = 'store_true', default = False, required = False)

unlink_parser = command_parser.add_parser('unlink')
unlink_parser.add_argument('-m', '--mapfile', required = False)

diffuse_parser = command_parser.add_parser('diffuse')
diffuse_parser.add_argument('-m', '--mapfile', required = False)
diffuse_parser.add_argument('-f', '--force', action = 'store_true', default = False, required = False)
