from argparse import Namespace
from configparser import ConfigParser
import os
import shutil
from syndot.colors import Color


VALID_PROMPT_CHOICES = {'y': True, 'ye': True, 'yes': True, 'n': False, 'no': False}


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


def generate_backup_path(path: str) -> str:
    backup_extension = ''
    if os.path.isfile(path):
        backup_extension = '.bak'
    elif os.path.isdir(path):
        backup_extension = '_bak'
    parent, target = os.path.split(path)
    return os.path.join(parent, target + backup_extension)


def copy(source: str, destination: str) -> None:
    destination_parent = os.path.dirname(destination)
    if not os.path.exists(destination_parent):
        os.makedirs(destination_parent)

    if os.path.isfile(source):
        shutil.copy2(source, destination)
    elif os.path.isdir(source):
        shutil.copytree(source, destination, symlinks = True)
        st = os.stat(source)
        os.chown(destination, st.st_uid, st.st_gid)


def change_parent_owner(source: str, destination: str, settings_dir: str):
    protected_directories = (expand_home_path(settings_dir), expand_home_path('~'), '/')
    while destination not in protected_directories:
        st = os.stat(source)
        os.chown(destination, st.st_uid, st.st_gid)
        source = os.path.dirname(source)
        destination = os.path.dirname(destination)


def change_child_owner(source: str, destination: str):
    source_content = os.listdir(source)
    destination_content = os.listdir(destination)
    for source_target, destination_target in zip(source_content, destination_content):
        source_target_path = os.path.join(source, source_target)
        destination_target_path = os.path.join(destination, destination_target)
        st = os.stat(source_target_path)
        os.chown(destination_target_path, st.st_uid, st.st_gid)
        if os.path.isdir(destination_target_path):
            change_child_owner(source = source_target_path, destination = destination_target_path)


def remove(path: str) -> None:
    if os.path.exists(path):
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def split_path(path: str) -> list[str]:
    return path.split(os.path.sep)[1:]


def expand_home_path(path: str) -> str:
    sudo_user = os.getenv('SUDO_USER')
    if sudo_user:
        if '~' in path:
            home = os.path.join(os.path.sep, 'home', sudo_user)
            return path.replace('~', home)
        else:
            return path
    else:
        return os.path.expanduser(path)


def compose_target_paths(settings_dir: str, target: str) -> tuple[str, str]:
    system_target_path = expand_home_path(target)
    settings_dir = expand_home_path(settings_dir)
    settings_target_path = os.path.join(settings_dir, *split_path(system_target_path))
    return system_target_path, settings_target_path


def ask_to_proceed() -> bool:
    choice = ''
    while choice not in VALID_PROMPT_CHOICES:
        choice = input("Do you want to proceed (y/N)? ").lower()
        if choice == '':
            choice = 'n'

    return VALID_PROMPT_CHOICES[choice]


def print_action(action_type: str, system_target_path: str, settings_target_path: str) -> None:
    if action_type == 'link':
        action = 'Linking'
        preposition = 'to'
        print(f"{action} {Color.link(system_target_path)} {preposition} {Color.settings(settings_target_path)}")
    elif action_type == 'unlink':
        action = 'Unlinking'
        preposition = 'from'
        print(f"{action} {Color.link(system_target_path)} {preposition} {Color.settings(settings_target_path)}")
    elif action_type == 'diffuse':
        action = 'Diffusing'
        preposition = 'to'
        print(f"{action} {Color.settings(settings_target_path)} {preposition} {Color.link(system_target_path)}")


def print_relationship(system_target_path: str, settings_target_path: str, symbol: str) -> None:
    print(f"{Color.link(system_target_path)} {Color.symbol(symbol)} {Color.settings(settings_target_path)}")


def print_highlight(sentence: str) -> None:
    print(f"{Color.highlight(sentence)}")
