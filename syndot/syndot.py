from argparse import ArgumentParser
import os


parser = ArgumentParser()
command_parser = parser.add_subparsers(dest = 'command')

init_parser = command_parser.add_parser('init')
init_parser.add_argument('-p', '--path', required = False)

args = parser.parse_args()


if args.command == 'init':
    destination = args.path if args.path is not None else os.path.expanduser('~/Settings')
    if os.path.exists(destination):
        raise ValueError(f"Destination folder {destination} already exists.")
    os.mkdir(destination)
