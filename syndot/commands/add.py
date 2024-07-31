from argparse import Namespace
import os
from syndot.utils.map_file import read_map_file, write_map_file
from syndot.utils.path import expand_home_path


def add(args: Namespace) -> None:
    map_file_path = expand_home_path(
        args.mapfile if args.mapfile is not None else 'map.ini'
    )

    config = read_map_file(map_file_path=map_file_path)
    current_targets = dict(config['Targets'])
    for label, paths in current_targets.items():
        current_targets[label] = paths.split()

    for target_path in args.path:
        if target_path.endswith(os.sep):
            target_path = target_path[:-1]

        if not os.path.exists(target_path):
            raise OSError(f"Target {target_path} not found")

        target_path = expand_home_path(target_path)
        if args.label in current_targets.keys():
            if target_path in current_targets[args.label]:
                print(f"Target {target_path} already in map file associated "
                      f"to label {args.label!r}")
                continue

        if target_path in [path for target in current_targets.values()
                           for path in target]:
            for label, paths in current_targets.items():
                if target_path in paths:
                    print(f"Target {target_path} already in map file "
                          f"associated to label {label!r}")
            continue

        if args.label not in current_targets.keys():
            current_targets[args.label] = []
        current_targets[args.label].append(target_path)

    if args.label not in current_targets.keys():
        current_targets[args.label] = []
    current_targets[args.label] = list(set(current_targets[args.label]))
    current_targets[args.label].sort()
    current_targets = dict(sorted(current_targets.items()))
    config['Targets'].clear()
    for label, paths in current_targets.items():
        config['Targets'][label] = '\n' + '\n'.join(paths)

    write_map_file(map_file_path=map_file_path, config=config)
