from argparse import Namespace
from syndot import utils
from syndot.colors import Color


def list_(args: Namespace) -> None:
    config = utils.read_map_file(map_file_path = args.mapfile)

    settings_dir = utils.expand_home_path(config['Path']['settings_dir'])
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    targets = [*target_directories, *target_files]
    targets.sort()

    for target in targets:
        print(target)
    utils.print_highlight("Settings directory:", end = ' ')
    print(Color.settings(settings_dir))
