from argparse import Namespace
import os
from syndot import utils


def remove(args: Namespace) -> None:
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')

    config = utils.read_map_file(map_file_path = map_file_path)
    current_files = config['Targets']['files'].split()
    current_directories = config['Targets']['directories'].split()
    target = args.target
    if target in current_files:
        current_files.remove(target)
        config['Targets']['files'] = '\n' + '\n'.join(current_files)
    elif target in current_directories:
        current_directories.remove(target)
        config['Targets']['directories'] = '\n' + '\n'.join(current_directories)
    else:
        raise NameError(f"Target {target} not found in map file")

    utils.write_map_file(map_file_path = map_file_path, config = config)
