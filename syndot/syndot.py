from argparse import ArgumentParser


parser = ArgumentParser()
command_parser = parser.add_subparsers(dest = 'command')

args = parser.parse_args()
