import os
from syndot.utils.path import expand_home_path
from syndot.utils.file_actions import copy


SOURCE_PATH = os.path.dirname(__file__)
HOME_PATH = expand_home_path('~')
CONFIG_DIR_PATH = os.path.join(HOME_PATH, '.config', 'syndot')
LOG_FILE_PATH = os.path.join(
    HOME_PATH,
    '.local',
    'share',
    'syndot',
    'log_file.log'
)


def copy_sources(source: str, destination: str) -> None:
    source_path = os.path.join(SOURCE_PATH, source)
    destination_path = os.path.join(CONFIG_DIR_PATH, destination)
    copy(source_path, destination_path)


def init_config() -> None:
    if not os.path.exists(CONFIG_DIR_PATH):
        copy_sources(source='_templates', destination='templates')
        copy_sources(source='_colorschemes', destination='colorschemes')

    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(os.path.dirname(LOG_FILE_PATH))
        with open(LOG_FILE_PATH, 'w') as log_file:
            log_file.write('')
