from argparse import ArgumentParser
from configparser import ConfigParser
import os
import shutil
from syndot import utils


parser = ArgumentParser()
command_parser = parser.add_subparsers(dest = 'command')

init_parser = command_parser.add_parser('init')
init_parser.add_argument('-p', '--path', required = False)

link_parser = command_parser.add_parser('link')
link_parser.add_argument('-m', '--mapfile', required = False)
link_parser.add_argument('-b', '--backup', action = 'store_true', default = False, required = False)

unlink_parser = command_parser.add_parser('unlink')
unlink_parser.add_argument('-m', '--mapfile', required = False)

diffuse_parser = command_parser.add_parser('diffuse')
diffuse_parser.add_argument('-m', '--mapfile', required = False)
diffuse_parser.add_argument('-f', '--force', action = 'store_true', default = False, required = False)

args = parser.parse_args()

VALID_CHOICES = {'y': True, 'ye': True, 'yes': True, 'n': False, 'no': False}
DEFAULT_DESTINATION = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join('..', 'templates', 'map.ini')


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
    destination = os.path.expanduser(args.path if args.path is not None else DEFAULT_DESTINATION)
    if os.path.exists(destination):
        raise ValueError(f"Destination directory {destination} already exists.")
    os.mkdir(destination)

    config = ConfigParser()
    config.read(MAP_TEMPLATE_PATH)
    config['Paths']['destination'] = destination

    with open(os.path.join(destination, 'map.ini'), 'w') as map_file:
        config.write(map_file)

elif args.command == 'link':
    source, destination, targets = read_map_file()

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if not os.path.exists(destination_target_path):
            if args.backup:
                utils.copy(source = source_target_path, destination = destination_target_path)
                backup_path = utils.generate_backup_path(path = source_target_path)
                os.rename(source_target_path, backup_path)
            else:
                shutil.move(source_target_path, destination_target_path)
            os.symlink(destination_target_path, source_target_path)

elif args.command == 'unlink':
    source, destination, targets = read_map_file()

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        utils.remove(path = source_target_path)
        shutil.move(destination_target_path, source_target_path)
        backup_path = utils.generate_backup_path(path = source_target_path)
        utils.remove(path = backup_path)

elif args.command == 'diffuse':
    source, destination, targets = read_map_file()

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if not os.path.exists(source_target_path):
            os.symlink(destination_target_path, source_target_path)
        else:
            if args.force:
                utils.remove(path = source_target_path)
                os.symlink(destination_target_path, source_target_path)
            else:
                force_diffuse = ''
                prompt_question = ''
                if os.path.isfile(source_target_path):
                    prompt_question = f"Source file {target} already exists. Force diffuse (Y/n)? "
                elif os.path.isdir(source_target_path):
                    prompt_question = f"Source directory {target} already exists. Force diffuse (Y/n)? "
                while force_diffuse not in VALID_CHOICES:
                    force_diffuse = input(prompt_question).lower()
                    if force_diffuse == '':
                        force_diffuse = 'y'
                if VALID_CHOICES[force_diffuse]:
                    utils.remove(path = source_target_path)
                    os.symlink(destination_target_path, source_target_path)
