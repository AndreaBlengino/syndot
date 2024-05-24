from configparser import ConfigParser
import os
import shutil
from tests.conftest import create_file_or_directory


TEST_DATA_PATH = 'test_data'
SETTINGS_DIR = os.path.join(TEST_DATA_PATH, 'Settings')
MAP_FILE_PATH = os.path.join(os.getcwd(), 'syndot', '_templates', 'map.ini')
TEST_MAP_FILE_PATH = os.path.join(os.getcwd(), TEST_DATA_PATH, 'map_test.ini')


def generate_testing_map_file() -> None:
    create_file_or_directory(TEST_MAP_FILE_PATH, is_file = True)
    with open(MAP_FILE_PATH, 'r') as map_file:
        lines = map_file.readlines()

    with open(TEST_MAP_FILE_PATH, 'w') as test_map_file:
        for line in lines:
            test_map_file.write(line.replace('~', os.path.join(os.getcwd(), TEST_DATA_PATH)))


def copy(source: str, destination: str) -> None:
    destination_parent = os.path.dirname(destination)
    if not os.path.exists(destination_parent):
        os.makedirs(destination_parent)

    if os.path.isfile(source):
        shutil.copy2(source, destination)
    elif os.path.isdir(source):
        shutil.copytree(source, destination, symlinks = True)


def remove(path: str) -> None:
    if os.path.exists(path):
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def create_parent_directory(path: str) -> None:
    parent_path = os.path.dirname(path)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)


def generate_link_testing_system_files(status: str) -> None:
    config = ConfigParser()
    config.read(TEST_MAP_FILE_PATH)

    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()

    if status == 'targets_to_be_linked':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                create_file_or_directory(path = target, is_file = is_file)
    elif status == 'already_existing_settings':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = target, is_file = is_file)
                create_file_or_directory(path = settings_target_path, is_file = is_file)
    elif status == 'missing_system_targets':
        return
    elif status == 'already_linked_targets':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
                create_parent_directory(path = target)
                os.symlink(settings_target_path, target)
    elif status == 'corrupted_targets':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_parent_directory(path = target)
                os.symlink(settings_target_path, target)
    elif status == 'wrong_existing_links':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
                create_parent_directory(path = target)
                os.symlink(os.path.join(settings_target_path + '.other'), target)


def generate_unlink_testing_system_files(status: str) -> None:
    config = ConfigParser()
    config.read(TEST_MAP_FILE_PATH)

    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()

    if status == 'targets_to_be_unlinked':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
                create_parent_directory(path = target)
                os.symlink(settings_target_path, target)
    elif status == 'wrong_existing_links':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
                create_parent_directory(path = target)
                os.symlink(os.path.join(settings_target_path + '.other'), target)
    elif status == 'missing_system_targets':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
    elif status == 'already_existing_system':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = target, is_file = is_file)
                create_file_or_directory(path = settings_target_path, is_file = is_file)
    elif status == 'already_unlinked_targets':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                create_file_or_directory(path = target, is_file = is_file)
    elif status == 'missing_settings_targets':
        return
    elif status == 'settings_are_links':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                other_target = settings_target_path + '.other'
                create_file_or_directory(path = other_target, is_file = is_file)
                os.symlink(other_target, settings_target_path)


def generate_diffuse_testing_system_files(status: str) -> None:
    config = ConfigParser()
    config.read(TEST_MAP_FILE_PATH)

    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()

    if status == 'targets_to_be_diffused':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
    elif status == 'already_existing_system':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = target, is_file = is_file)
                create_file_or_directory(path = settings_target_path, is_file = is_file)
    elif status == 'already_diffused_targets':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
                create_parent_directory(path = target)
                os.symlink(settings_target_path, target)
    elif status == 'wrong_existing_links':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                create_file_or_directory(path = settings_target_path, is_file = is_file)
                create_parent_directory(path = target)
                os.symlink(os.path.join(settings_target_path + '.other'), target)
    elif status == 'missing_settings_targets':
        return
    elif status == 'settings_are_links':
        for target_list, is_file in zip([target_files, target_directories], [True, False]):
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                other_target = settings_target_path + '.other'
                create_file_or_directory(path = other_target, is_file = is_file)
                os.symlink(other_target, settings_target_path)


def generate_add_and_remove_testing_system_files() -> None:
    config = ConfigParser()
    config.read(TEST_MAP_FILE_PATH)
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    for target_list, is_file in zip([target_files, target_directories], [True, False]):
        for target in target_list:
            create_file_or_directory(path = target, is_file = is_file)


def empty_testing_map_file() -> None:
    config = ConfigParser()
    config.read(TEST_MAP_FILE_PATH)
    config['Targets']['directories'] = ''
    config['Targets']['files'] = ''
    with open(TEST_MAP_FILE_PATH, 'w') as map_file:
        config.write(map_file)
