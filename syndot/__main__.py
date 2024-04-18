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

unlink_parser = command_parser.add_parser('unlink')
unlink_parser.add_argument('-m', '--mapfile', required = False)

args = parser.parse_args()


def read_map_file() -> tuple[str, str, list[str]]:
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Missing map.ini file in current directory.")
    config = ConfigParser()
    config.read(map_file_path)
    source = config['Paths']['source']
    destination = config['Paths']['destination']
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    targets = [*target_files, *target_directories]

    return source, destination, targets


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
    source, destination, targets = read_map_file()

    for target in targets:
        source_target_path = os.path.join(os.path.expanduser(source), target)
        destination_target_path = os.path.join(os.path.expanduser(destination), target)
        if not os.path.exists(destination_target_path):
            if args.backup:
                backup_extension = ''
                if os.path.isfile(source_target_path):
                    shutil.copy(source_target_path, destination_target_path)
                    backup_extension = '.bak'
                elif os.path.isdir(source_target_path):
                    shutil.copytree(source_target_path, destination_target_path)
                    backup_extension = '_bak'
                os.rename(source_target_path, os.path.join(os.path.expanduser(source), target + backup_extension))
            else:
                shutil.move(source_target_path, destination_target_path)
            os.symlink(destination_target_path, source_target_path)

elif args.command == 'unlink':
    source, destination, targets = read_map_file()

    for target in targets:
        source_target_path = os.path.join(os.path.expanduser(source), target)
        destination_target_path = os.path.join(os.path.expanduser(destination), target)

        if os.path.exists(source_target_path):
            os.unlink(source_target_path)

        shutil.move(destination_target_path, source_target_path)

        if os.path.isfile(source_target_path):
            backup_path = os.path.join(os.path.expanduser(source), target + '.bak')
            if os.path.exists(backup_path):
                os.remove(backup_path)
        elif os.path.isdir(source_target_path):
            backup_path = os.path.join(os.path.expanduser(source), target + '_bak')
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
