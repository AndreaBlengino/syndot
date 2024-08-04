from argparse import Namespace
from configparser import ConfigParser
import os
from syndot.init_config import CONFIG_DIR_PATH
from syndot.utils.path import expand_home_path
from syndot.utils.map_file import read_map_file, write_map_file


DEFAULT_SETTINGS_DIR = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join(CONFIG_DIR_PATH, 'templates', 'map.ini')
if (not os.path.exists(CONFIG_DIR_PATH) or
        not os.path.exists(MAP_TEMPLATE_PATH)):
    MAP_TEMPLATE_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '_templates',
        'map.ini'
    )


def init(args: Namespace) -> None:
    settings_dir = expand_home_path(
        args.path if args.path is not None else DEFAULT_SETTINGS_DIR
    )
    if os.path.exists(settings_dir):
        raise ValueError(f"Settings directory {settings_dir} already exists.")
    os.makedirs(settings_dir)

    config = read_map_file(MAP_TEMPLATE_PATH)
    config['Path']['settings_dir'] = settings_dir

    _expand_default_target_path(config=config)

    write_map_file(
        map_file_path=os.path.join(settings_dir, 'map.ini'),
        config=config
    )


def _expand_default_target_path(config: ConfigParser) -> None:
    for label, paths in config['Targets'].items():
        paths = [expand_home_path(path) for path in paths.split()]
        paths = list(set(paths))
        paths.sort()
        config['Targets'][label] = '\n' + '\n'.join(paths)
