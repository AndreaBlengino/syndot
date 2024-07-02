from configparser import ConfigParser
from hypothesis.strategies import (composite, text, lists, characters,
                                   sampled_from)
import os
import shutil


TEST_DATA_PATH = 'test_data'
SETTINGS_DIR = os.path.join(TEST_DATA_PATH, 'Settings')
MAP_FILE_PATH = os.path.join(os.getcwd(), 'syndot', '_templates', 'map.ini')


def get_valid_targets() -> list[str]:
    config = ConfigParser()
    config.read(MAP_FILE_PATH)
    valid_labels = list(config['Targets'].keys())
    valid_targets = []
    for target in config['Targets'].values():
        valid_targets.extend(target.split())

    return valid_labels, valid_targets


valid_labels, valid_targets = get_valid_targets()


def create_file_or_directory(path: str, is_file: bool) -> None:
    if is_file:
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as file:
            file.write('')
    else:
        if not os.path.exists(path):
            os.makedirs(path)


@composite
def paths(draw, absolute=False):
    folder_list = draw(lists(elements=text(min_size=5,
                                           max_size=10,
                                           alphabet=characters(
                                               min_codepoint=97,
                                               max_codepoint=122)),
                             min_size=2,
                             max_size=5))
    if absolute:
        folder_list.insert(0, os.path.join(os.getcwd(), TEST_DATA_PATH))
    else:
        folder_list.insert(0, os.path.join('.', TEST_DATA_PATH))

    return os.path.join(*folder_list)


@composite
def usernames(draw):
    return draw(text(min_size=5,
                     max_size=10,
                     alphabet=characters(min_codepoint=97,
                                         max_codepoint=122)))


@composite
def labels(draw):
    return draw(sampled_from(elements=valid_labels))


@composite
def targets(draw, absolute=True):
    if absolute:
        return draw(sampled_from(elements=valid_targets))
    else:
        return draw(sampled_from(
            elements=[target.replace(
                '~', os.path.join(os.getcwd(), TEST_DATA_PATH))
                for target in valid_targets]))


def reset_environment():
    if os.path.exists(TEST_DATA_PATH):
        shutil.rmtree(TEST_DATA_PATH)
