from argparse import Namespace
from syndot.utils.map_file import read_map_file
from syndot.utils.path import expand_home_path
from syndot.utils.print_ import print_highlight
from syndot.utils.colors import Color


def list_(args: Namespace) -> None:
    config = read_map_file(map_file_path=args.mapfile)

    settings_dir = expand_home_path(config['Path']['settings_dir'])
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    targets = [*target_directories, *target_files]
    targets.sort()

    for target in targets:
        print(target)
    print_highlight("Settings directory:", end=' ')
    print(Color.settings(settings_dir))
