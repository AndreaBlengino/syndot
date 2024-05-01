from argparse import Namespace
import os
from syndot import utils


DEFAULT_SETTINGS_DIR = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join('templates', 'map.ini')


def init(args: Namespace) -> None:
    settings_dir = os.path.expanduser(args.path if args.path is not None else DEFAULT_SETTINGS_DIR)
    if os.path.exists(settings_dir):
        raise ValueError(f"Settings directory {settings_dir} already exists.")
    os.mkdir(settings_dir)

    config = utils.read_map_file(MAP_TEMPLATE_PATH)
    config['Path']['settings_dir'] = settings_dir

    utils.write_map_file(map_file_path = os.path.join(settings_dir, 'map.ini'), config = config)
