from argparse import Namespace
from configparser import ConfigParser
import os
from syndot.utils.path import expand_home_path


def read_map_file(map_file_path: str | None) -> ConfigParser:
    map_file_path = expand_home_path(map_file_path if map_file_path is not None else 'map.ini')
    if not os.path.exists(map_file_path):
        if map_file_path == 'map.ini':
            raise FileNotFoundError("Missing map.ini file in current directory.")
        else:
            raise FileNotFoundError("Missing map.ini file at the specified path.")
    config = ConfigParser()
    config.read(map_file_path)

    return config


def get_map_info(config: ConfigParser, args: Namespace) -> tuple[str, list[str]]:
    settings_dir = config['Path']['settings_dir']
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    if args.TARGET_PATH_START is None and args.all:
        targets = [*target_files, *target_directories]
    else:
        targets = []
        for file in target_files:
            if args.exact:
                if file == args.TARGET_PATH_START:
                    targets.append(file)
            else:
                if file.startswith(args.TARGET_PATH_START):
                    targets.append(file)
        for directory in target_directories:
            if args.exact:
                if directory == args.TARGET_PATH_START:
                    targets.append(directory)
            else:
                if directory.startswith(args.TARGET_PATH_START):
                    targets.append(directory)

    return settings_dir, targets


def write_map_file(map_file_path: str | None, config: ConfigParser) -> None:
    with open(map_file_path, 'w') as map_file:
        config.write(map_file)
