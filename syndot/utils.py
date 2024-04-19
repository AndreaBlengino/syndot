from configparser import ConfigParser
import os
import shutil


def read_map_file(map_file: str | None) -> tuple[str, str, list[str]]:
    map_file_path = os.path.expanduser(map_file if map_file is not None else 'map.ini')
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Missing map.ini file in current directory.")
    config = ConfigParser()
    config.read(map_file_path)
    source = config['Paths']['source']
    destination = config['Paths']['destination']
    target_directories = config['Targets']['directories'].split()
    target_files = config['Targets']['files'].split()
    targets = [*target_files, *target_directories]

    return source, destination, targets


def generate_backup_path(path: str) -> str:
    backup_extension = ''
    if os.path.isfile(path):
        backup_extension = '.bak'
    elif os.path.isdir(path):
        backup_extension = '_bak'
    parent, target = os.path.split(path)
    return os.path.join(parent, target + backup_extension)


def copy(source: str, destination: str) -> None:
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