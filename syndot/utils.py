from configparser import ConfigParser
import os
import shutil


VALID_PROMPT_CHOICES = {'y': True, 'ye': True, 'yes': True, 'n': False, 'no': False}


def read_map_file(map_file_path: str | None) -> ConfigParser:
    map_file_path = os.path.expanduser(map_file_path if map_file_path is not None else 'map.ini')
    if not os.path.exists(map_file_path):
        if map_file_path == 'map.ini':
            raise FileNotFoundError("Missing map.ini file in current directory.")
        else:
            raise FileNotFoundError("Missing map.ini file at the specified path.")
    config = ConfigParser()
    config.read(map_file_path)

    return config


def get_map_info(config: ConfigParser) -> tuple[str, str, list[str]]:
    source = config['Paths']['source']
    destination = config['Paths']['destination']
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    targets = [*target_files, *target_directories]

    return source, destination, targets


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
    if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))

    if os.path.isfile(source):
        shutil.copy(source, destination)
    elif os.path.isdir(source):
        shutil.copytree(source, destination)


def remove(path: str) -> None:
    if os.path.exists(path):
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def compose_target_paths(source: str, destination: str, target: str) -> tuple[str, str]:
    source_target_path = os.path.join(os.path.expanduser(source), target)
    destination_target_path = os.path.join(os.path.expanduser(destination), target)
    return source_target_path, destination_target_path


def compose_force_question(target_path: str, target_is_source: bool, command: str) -> str:
    question = ''
    target_type = 'Source' if target_is_source else 'Destination'
    if os.path.isfile(target_path):
        question = f"{target_type} file {target_path} already exists. Force {command}"
    elif os.path.isdir(target_path):
        question = f"{target_type} directory {target_path} already exists. Force {command}"
    return question


def prompt_question(question: str, default: str | None = None) -> bool:
    choice = ''
    if default is not None:
        if VALID_PROMPT_CHOICES[default]:
            default_text = ' (Y/n)? '
        else:
            default_text = ' (y/N)? '
    else:
        default_text = ' (y/n)? '
    while choice not in VALID_PROMPT_CHOICES:
        choice = input(question + default_text).lower()
        if default is not None and choice == '':
            choice = default

    return VALID_PROMPT_CHOICES[choice]
