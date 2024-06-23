from argparse import Namespace
import os
from syndot.utils.map_file import read_map_file, write_map_file
from syndot.utils.path import expand_home_path


def add(args: Namespace) -> None:
    map_file_path = expand_home_path(
        args.mapfile if args.mapfile is not None else 'map.ini')

    target = args.TARGET_PATH
    if target.endswith(os.sep):
        target = target[:-1]
    if not os.path.exists(target):
        raise OSError(f"Target {target} not found")

    config = read_map_file(map_file_path=map_file_path)
    current_targets = []
    if os.path.isfile(target):
        current_targets = config['Targets']['files'].split()
    elif os.path.isdir(target):
        current_targets = config['Targets']['directories'].split()

    target_path = expand_home_path(target)
    if target_path in current_targets:
        print(f"Target {target} already in map file")
        return
    current_targets.append(target_path)
    current_targets = list(set(current_targets))
    current_targets.sort()

    if os.path.isfile(target):
        config['Targets']['files'] = '\n' + '\n'.join(current_targets)
    elif os.path.isdir(target):
        config['Targets']['directories'] = '\n' + '\n'.join(current_targets)

    write_map_file(map_file_path=map_file_path, config=config)
