from argparse import Namespace
import os
from syndot.utils.map_file import read_map_file, write_map_file
from syndot.utils.path import expand_home_path


def remove(args: Namespace) -> None:
    map_file_path = expand_home_path(
        args.mapfile if args.mapfile is not None else 'map.ini'
    )

    config = read_map_file(map_file_path=map_file_path)
    current_targets = dict(config['Targets'])
    for label, paths in current_targets.items():
        current_targets[label] = paths.split()

    if args.label is not None:
        for label in args.label:
            if label in current_targets.keys():
                current_targets.pop(label)
            else:
                raise NameError(f"Label {label} not found in map file")

    if args.path is not None:
        for path in args.path:
            path_removed = False
            if path.endswith(os.sep):
                path = path[:-1]
            for current_paths in current_targets.values():
                if path in current_paths:
                    current_paths.remove(path)
                    path_removed = True
            if not path_removed:
                raise NameError(f"Path {path} not found in map file")

    current_targets = dict(sorted(current_targets.items()))
    config['Targets'].clear()
    for label, paths in current_targets.items():
        paths = list(set(paths))
        paths.sort()
        config['Targets'][label] = '\n' + '\n'.join(paths)

    write_map_file(map_file_path=map_file_path, config=config)
