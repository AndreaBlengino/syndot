import os


def generate_backup_path(path: str) -> str:
    backup_extension = ''
    if os.path.isfile(path):
        backup_extension = '.bak'
    elif os.path.isdir(path):
        backup_extension = '_bak'
    parent, target = os.path.split(path)
    return os.path.join(parent, target + backup_extension)


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
    settings_target_path = os.path.join(
        settings_dir, *split_path(system_target_path))
    return system_target_path, settings_target_path
