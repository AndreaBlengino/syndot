from argparse import Namespace
from configparser import ConfigParser
import os
from syndot import utils


DEFAULT_SETTINGS_DIR = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_templates', 'map.ini')


def init(args: Namespace) -> None:
    settings_dir = utils.expand_home_path(args.path if args.path is not None else DEFAULT_SETTINGS_DIR)
    if os.path.exists(settings_dir):
        raise ValueError(f"Settings directory {settings_dir} already exists.")
    os.mkdir(settings_dir)

    config = utils.read_map_file(MAP_TEMPLATE_PATH)
    config['Path']['settings_dir'] = settings_dir

    expand_default_target_path(config = config, target_category = 'files')
    expand_default_target_path(config = config, target_category = 'directories')

    utils.write_map_file(map_file_path = os.path.join(settings_dir, 'map.ini'), config = config)


def expand_default_target_path(config: ConfigParser, target_category: str):
    targets = [utils.expand_home_path(target) for target in config['Targets'][target_category].split()]
    targets = list(set(targets))
    targets.sort()
    config['Targets'][target_category] = '\n' + '\n'.join(targets)
