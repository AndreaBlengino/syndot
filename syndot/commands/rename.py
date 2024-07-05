from argparse import Namespace
from syndot.utils.map_file import read_map_file, write_map_file
from syndot.utils.path import expand_home_path


def rename(args: Namespace) -> None:
    map_file_path = expand_home_path(
        args.mapfile if args.mapfile is not None else 'map.ini')

    config = read_map_file(map_file_path=map_file_path)

    targets = dict(config['Targets'])

    if args.old_label in targets.keys():
        targets[args.new_label] = targets.pop(args.old_label)
    else:
        raise KeyError(f"Label {args.old_label!r} not found in the map file")

    targets = dict(sorted(targets.items()))
    config['Targets'].clear()
    for label, paths in targets.items():
        config['Targets'][label] = paths

    write_map_file(map_file_path=map_file_path, config=config)
