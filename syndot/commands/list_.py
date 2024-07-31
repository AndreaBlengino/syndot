from argparse import Namespace
from syndot.utils.map_file import read_map_file
from syndot.utils.path import expand_home_path
from syndot.utils.print_ import print_highlight
from syndot.utils.colors import Color


def list_(args: Namespace) -> None:
    config = read_map_file(map_file_path=args.mapfile)

    settings_dir = expand_home_path(config['Path']['settings_dir'])
    targets = dict(config['Targets'])

    if args.label:
        for label in targets.keys():
            _list_labels(label=label)
        if args.directory:
            _print_settings_directory(settings_dir=settings_dir)
        return

    if args.path:
        for paths in targets.values():
            _list_paths(paths=paths, indent=False)
        if args.directory:
            _print_settings_directory(settings_dir=settings_dir)
        return

    if args.search:
        if args.search not in targets.keys():
            raise NameError(f"Label {args.search} not found in map file")

        _list_labels(label=args.search)
        _list_paths(paths=targets[args.search], indent=True)
        if args.directory:
            _print_settings_directory(settings_dir=settings_dir)
        return

    for label, paths in targets.items():
        _list_labels(label=label)
        _list_paths(paths=paths, indent=True)
        print()
    if args.directory:
        _print_settings_directory(settings_dir=settings_dir)


def _list_labels(label: str) -> None:
    print(label.split()[0])


def _list_paths(paths: str, indent: bool) -> None:
    paths = paths.split()
    for path in paths:
        if indent:
            print(f"    {path}")
        else:
            print(path)


def _print_settings_directory(settings_dir: str) -> None:
    print_highlight("Settings directory:", end=' ')
    print(Color.settings(settings_dir))
