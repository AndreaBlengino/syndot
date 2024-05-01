from argparse import Namespace
import os
import shutil
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


def link(args: Namespace) -> None:
    settings_dir, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                               target = args.target)

    for target in targets:
        system_target_path, settings_target_path = utils.compose_target_paths(settings_dir = settings_dir,
                                                                              target = target)
        if not os.path.islink(system_target_path):
            if os.path.exists(system_target_path):
                if not os.path.exists(settings_target_path):
                    link_dotfile(settings_dir = settings_dir,
                                 system_target_path = system_target_path,
                                 settings_target_path = settings_target_path,
                                 backup = args.backup)
                else:
                    if args.force:
                        utils.remove(path = settings_target_path)
                        link_dotfile(settings_dir = settings_dir,
                                     system_target_path = system_target_path,
                                     settings_target_path = settings_target_path,
                                     backup = args.backup)
                    else:
                        question = utils.compose_force_question(target_path = settings_target_path,
                                                                target_is_in_system = False,
                                                                command = args.command)
                        force_link = utils.prompt_question(question = question, default = 'n')
                        if force_link:
                            utils.remove(path = settings_target_path)
                            link_dotfile(settings_dir = settings_dir,
                                         system_target_path = system_target_path,
                                         settings_target_path = settings_target_path,
                                         backup = args.backup)
            else:
                print(f"Skipping missing {system_target_path}")
        else:
            if os.readlink(system_target_path) == settings_target_path:
                if os.path.exists(system_target_path):
                    print(f"Skipping already linked {system_target_path}")
                else:
                    print(f"{system_target_path} is a symlink to {settings_target_path}, which is missing")
            else:
                if not os.path.islink(settings_target_path):
                    if os.path.exists(settings_target_path):
                        if args.force:
                            utils.remove(path = system_target_path)
                            diffuse_dotfile(system_target_path = system_target_path,
                                            settings_target_path = settings_target_path)
                            if args.backup:
                                backup_path = utils.generate_backup_path(path = system_target_path)
                                utils.copy(source = settings_target_path, destination = backup_path)
                        else:
                            question = f"{system_target_path} is a symlink to {os.readlink(system_target_path)}, " \
                                       f"not to {settings_target_path} \nForce link to {settings_target_path}"
                            force_link = utils.prompt_question(question = question, default = 'n')
                            if force_link:
                                utils.remove(path = system_target_path)
                                diffuse_dotfile(system_target_path = system_target_path,
                                                settings_target_path = settings_target_path)
                                if args.backup:
                                    backup_path = utils.generate_backup_path(path = system_target_path)
                                    utils.copy(source = settings_target_path, destination = backup_path)
                    else:
                        print(f"{system_target_path} is a symlink to {os.readlink(system_target_path)}, "
                              f"not to {settings_target_path}, which does not exists")
                else:
                    print(f"Skipping {system_target_path} because is a symlink to {os.readlink(system_target_path)} and"
                          f"{settings_target_path} is a symlink to {os.readlink(settings_target_path)}")


def unlink(args: Namespace) -> None:
    settings_dir, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                               target = args.target)

    for target in targets:
        system_target_path, settings_target_path = utils.compose_target_paths(settings_dir = settings_dir,
                                                                              target = target)
        if not os.path.islink(settings_target_path):
            if os.path.exists(settings_target_path):
                if os.path.islink(system_target_path):
                    if os.readlink(system_target_path) == settings_target_path:
                        unlink_dotfile(system_target_path = system_target_path,
                                       settings_target_path = settings_target_path,
                                       settings_dir = settings_dir)
                    else:
                        if args.force:
                            unlink_dotfile(system_target_path = system_target_path,
                                           settings_target_path = settings_target_path,
                                           settings_dir = settings_dir)
                        else:
                            question = f"{system_target_path} is a symlink to {os.readlink(system_target_path)}, " \
                                       f"not to {settings_target_path} \nForce unlink of {settings_target_path}"
                            force_unlink = utils.prompt_question(question = question, default = 'n')
                            if force_unlink:
                                unlink_dotfile(system_target_path = system_target_path,
                                               settings_target_path = settings_target_path,
                                               settings_dir = settings_dir)
                else:
                    if not os.path.exists(system_target_path):
                        unlink_dotfile(system_target_path = system_target_path,
                                       settings_target_path = settings_target_path,
                                       settings_dir = settings_dir)
                    else:
                        if args.force:
                            unlink_dotfile(system_target_path = system_target_path,
                                           settings_target_path = settings_target_path,
                                           settings_dir = settings_dir)
                        else:
                            question = f"{system_target_path} is not a symlink\n" \
                                       f"Force unlink of {settings_target_path}"
                            force_unlink = utils.prompt_question(question = question, default = 'n')
                            if force_unlink:
                                unlink_dotfile(system_target_path = system_target_path,
                                               settings_target_path = settings_target_path,
                                               settings_dir = settings_dir)
            else:
                print(f"Skipping missing {settings_target_path}")
        else:
            print(f"Skipping {settings_target_path} because is a symlink to {os.readlink(settings_target_path)}")


def diffuse(args: Namespace) -> None:
    settings_dir, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                               target = args.target)

    for target in targets:
        system_target_path, settings_target_path = utils.compose_target_paths(settings_dir = settings_dir,
                                                                              target = target)
        if not os.path.islink(settings_target_path):
            if os.path.exists(settings_target_path):
                if not os.path.islink(system_target_path):
                    if not os.path.exists(system_target_path):
                        diffuse_dotfile(system_target_path = system_target_path,
                                        settings_target_path = settings_target_path)
                    else:
                        if args.force:
                            utils.remove(system_target_path)
                            diffuse_dotfile(system_target_path = system_target_path,
                                            settings_target_path = settings_target_path)
                        else:
                            question = f"{system_target_path} already exists\n"\
                                       f"Force diffuse of {settings_target_path}"
                            force_diffuse = utils.prompt_question(question = question, default = 'n')
                            if force_diffuse:
                                utils.remove(system_target_path)
                                diffuse_dotfile(system_target_path = system_target_path,
                                                settings_target_path = settings_target_path)
                else:
                    if os.readlink(system_target_path) == settings_target_path:
                        print(f"Skipping {settings_target_path} because already linked by {system_target_path}")
                    else:
                        if args.force:
                            utils.remove(system_target_path)
                            diffuse_dotfile(system_target_path = system_target_path,
                                            settings_target_path = settings_target_path)
                        else:
                            question = f"{system_target_path} is a symlink to {os.readlink(system_target_path)}, " \
                                       f"not to {settings_target_path} \nForce diffuse of {settings_target_path}"
                            force_diffuse = utils.prompt_question(question = question, default = 'n')
                            if force_diffuse:
                                utils.remove(system_target_path)
                                diffuse_dotfile(system_target_path = system_target_path,
                                                settings_target_path = settings_target_path)
            else:
                print(f"Skipping missing {settings_target_path}")
        else:
            print(f"Skipping {settings_target_path} because is a symlink to {os.readlink(settings_target_path)}")


def add(args: Namespace) -> None:
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')

    target = args.target
    if not os.path.exists(target):
        raise OSError(f"Target {target} not found")

    config = utils.read_map_file(map_file_path = map_file_path)
    current_targets = []
    if os.path.isfile(target):
        current_targets = config['Targets']['files'].split()
    elif os.path.isdir(target):
        current_targets = config['Targets']['directories'].split()

    relative_target_path = os.path.expanduser(target).replace(os.path.expanduser(config['Paths']['source']), '')[1:]
    if relative_target_path in current_targets:
        print(f"Target {target} already in map file")
        return
    current_targets.append(relative_target_path)
    current_targets = list(set(current_targets))
    current_targets.sort()

    if os.path.isfile(target):
        config['Targets']['files'] = '\n' + '\n'.join(current_targets)
    elif os.path.isdir(target):
        config['Targets']['directories'] = '\n' + '\n'.join(current_targets)

    utils.write_map_file(map_file_path = map_file_path, config = config)


def remove(args: Namespace) -> None:
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')

    config = utils.read_map_file(map_file_path = map_file_path)
    current_files = config['Targets']['files'].split()
    current_directories = config['Targets']['directories'].split()
    target = args.target
    if target in current_files:
        current_files.remove(target)
        config['Targets']['files'] = '\n' + '\n'.join(current_files)
    elif target in current_directories:
        current_directories.remove(target)
        config['Targets']['directories'] = '\n' + '\n'.join(current_directories)
    else:
        raise NameError(f"Target {target} not found in map file")

    utils.write_map_file(map_file_path = map_file_path, config = config)


def link_dotfile(settings_dir: str, system_target_path: str, settings_target_path: str, backup: bool) -> None:
    if backup:
        utils.copy(source = system_target_path, destination = settings_target_path)
        utils.change_parent_owner(source = system_target_path, destination = settings_target_path,
                                  settings_dir = settings_dir)
        backup_path = utils.generate_backup_path(path = system_target_path)
        os.rename(system_target_path, backup_path)
    else:
        if not os.path.exists(os.path.dirname(settings_target_path)):
            os.makedirs(os.path.dirname(settings_target_path))
        shutil.move(system_target_path, settings_target_path)
    os.symlink(settings_target_path, system_target_path)


def unlink_dotfile(system_target_path: str, settings_target_path: str, settings_dir: str) -> None:
    utils.remove(path = system_target_path)
    shutil.move(settings_target_path, system_target_path)
    backup_path = utils.generate_backup_path(path = system_target_path)
    utils.remove(path = backup_path)

    parent_directory = os.path.dirname(settings_target_path)
    protected_directories = (settings_dir, utils.expand_home_path('~'), '/')
    while parent_directory not in protected_directories:
        parent_directory_content = os.listdir(parent_directory)
        if not parent_directory_content or ((len(parent_directory_content) == 1) and
                                            parent_directory_content[0] == '.directory'):
            shutil.rmtree(parent_directory)
            parent_directory = os.path.dirname(parent_directory)
        else:
            break


def diffuse_dotfile(system_target_path: str, settings_target_path: str) -> None:
    if not os.path.exists(os.path.dirname(system_target_path)):
        os.makedirs(os.path.dirname(system_target_path))
    os.symlink(settings_target_path, system_target_path)
