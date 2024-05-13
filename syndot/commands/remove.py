from argparse import Namespace
import os
from syndot.utils.map_file import read_map_file, write_map_file
from syndot.utils.path import expand_home_path


def remove(args: Namespace) -> None:
    map_file_path = expand_home_path(args.mapfile if args.mapfile is not None else 'map.ini')

    config = read_map_file(map_file_path = map_file_path)
    current_files = config['Targets']['files'].split()
    current_directories = config['Targets']['directories'].split()
    target = args.TARGET_PATH
    if target.endswith(os.sep):
        target = target[:-1]
    if target in current_files:
        current_files.remove(target)
        config['Targets']['files'] = '\n' + '\n'.join(current_files)
    elif target in current_directories:
        current_directories.remove(target)
        config['Targets']['directories'] = '\n' + '\n'.join(current_directories)
    else:
        raise NameError(f"Target {target} not found in map file")

    write_map_file(map_file_path = map_file_path, config = config)
