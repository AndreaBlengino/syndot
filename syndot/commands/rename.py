from argparse import Namespace
from syndot.utils.map_file import read_map_file, write_map_file
from syndot.utils.path import expand_home_path


def rename(args: Namespace) -> None:
    if args.old_label == args.new_label:
        raise NameError("The new label must be different from the old one")

    map_file_path = expand_home_path(
        args.mapfile if args.mapfile is not None else 'map.ini'
    )

    config = read_map_file(map_file_path=map_file_path)

    targets = dict(config['Targets'])

    if args.old_label in targets.keys():
        if args.new_label in targets.keys():
            paths = [*targets[args.old_label].split(),
                     *targets[args.new_label].split()]
            paths.sort()
            targets[args.new_label] = '\n' + '\n'.join(paths)
            targets.pop(args.old_label)
        else:
            targets[args.new_label] = targets.pop(args.old_label)
    else:
        raise KeyError(f"Label {args.old_label!r} not found in the map file")

    config['Targets'] = dict(sorted(targets.items()))

    write_map_file(map_file_path=map_file_path, config=config)
