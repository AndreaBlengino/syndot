from argparse import ArgumentParser
from configparser import ConfigParser
import os
import shutil


parser = ArgumentParser()
command_parser = parser.add_subparsers(dest = 'command')

init_parser = command_parser.add_parser('init')
init_parser.add_argument('-p', '--path', required = False)

link_parser = command_parser.add_parser('link')
link_parser.add_argument('-m', '--mapfile', required = False)
link_parser.add_argument('-b', '--backup', action = 'store_true', default = False, required = False)

args = parser.parse_args()


if args.command == 'init':
    destination = os.path.expanduser(args.path if args.path is not None else '~/Settings')
    if os.path.exists(destination):
        raise ValueError(f"Destination directory {destination} already exists.")
    os.mkdir(destination)

    config = ConfigParser()
    config.read(os.path.join('..', 'templates', 'map.ini'))
    config['Paths']['destination'] = destination

    with open(os.path.join(destination, 'map.ini'), 'w') as map_file:
        config.write(map_file)

elif args.command == 'link':
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Missing map.ini file in current directory.")
    config = ConfigParser()
    config.read(map_file_path)
    source = config['Paths']['source']
    destination = config['Paths']['destination']
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()

    for file in target_files:
        source_file_path = os.path.join(os.path.expanduser(source), file)
        destination_file_path = os.path.join(os.path.expanduser(destination), file)
        if args.backup:
            shutil.copy(source_file_path, destination_file_path)
            os.rename(source_file_path, os.path.join(os.path.expanduser(source), file + '.bak'))
        else:
            shutil.move(source_file_path, destination_file_path)
        os.symlink(destination_file_path, source_file_path)
