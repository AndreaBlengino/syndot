from argparse import Namespace
import os
import shutil
from syndot import utils


DEFAULT_DESTINATION = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join('..', 'templates', 'map.ini')


def init(args: Namespace) -> None:
    destination = os.path.expanduser(args.path if args.path is not None else DEFAULT_DESTINATION)
    if os.path.exists(destination):
        raise ValueError(f"Destination directory {destination} already exists.")
    os.mkdir(destination)

    config = utils.read_map_file(MAP_TEMPLATE_PATH)
    config['Paths']['destination'] = destination

    utils.write_map_file(map_file_path = os.path.join(destination, 'map.ini'), config = config)


def link(args: Namespace) -> None:
    source, destination, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                                      target = args.target)

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if not os.path.islink(source_target_path):
            if os.path.exists(source_target_path):
                if not os.path.exists(destination_target_path):
                    link_dotfile(source_target_path = source_target_path,
                                 destination_target_path = destination_target_path,
                                 backup = args.backup)
                else:
                    if args.force:
                        utils.remove(path = destination_target_path)
                        link_dotfile(source_target_path = source_target_path,
                                     destination_target_path = destination_target_path,
                                     backup = args.backup)
                    else:
                        question = utils.compose_force_question(target_path = destination_target_path,
                                                                target_is_source = False,
                                                                command = args.command)
                        force_link = utils.prompt_question(question = question, default = 'n')
                        if force_link:
                            utils.remove(path = destination_target_path)
                            link_dotfile(source_target_path = source_target_path,
                                         destination_target_path = destination_target_path,
                                         backup = args.backup)
            else:
                print(f"Skipping missing {source_target_path}")
        else:
            if os.readlink(source_target_path) == destination_target_path:
                if os.path.exists(source_target_path):
                    print(f"Skipping already linked {source_target_path}")
                else:
                    print(f"{source_target_path} is a symlink to the missing {destination_target_path}")
            else:
                if os.path.exists(destination_target_path):
                    question = f"{source_target_path} is a symlink to {os.readlink(source_target_path)}, " \
                               f"not to {destination_target_path} \nForce link to {destination_target_path}?"
                    force_link = utils.prompt_question(question = question, default = 'n')
                    if force_link:
                        utils.remove(path = source_target_path)
                        diffuse_dotfile(source_target_path = source_target_path,
                                        destination_target_path = destination_target_path)
                        if args.backup:
                            backup_path = utils.generate_backup_path(path = source_target_path)
                            utils.copy(source = destination_target_path, destination = backup_path)
                else:
                    print(f"{source_target_path} is a symlink to {os.readlink(source_target_path)}, "
                          f"not to {destination_target_path}, which does not exists")


def unlink(args: Namespace) -> None:
    source, destination, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                                      target = args.target)

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if os.path.exists(destination_target_path):
            unlink_dotfile(source_target_path = source_target_path,
                           destination_target_path = destination_target_path,
                           source = source,
                           destination = destination)
        else:
            raise FileNotFoundError(f"Missing {destination_target_path} in destination directory.")


def diffuse(args: Namespace) -> None:
    source, destination, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                                      target = args.target)

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if not os.path.exists(source_target_path):
            if os.path.exists(destination_target_path):
                diffuse_dotfile(source_target_path = source_target_path,
                                destination_target_path = destination_target_path)
            else:
                raise FileNotFoundError(f"Missing {destination_target_path} in destination directory.")
        else:
            if args.force:
                utils.remove(path = source_target_path)
                diffuse_dotfile(source_target_path = source_target_path,
                                destination_target_path = destination_target_path)
            else:
                question = utils.compose_force_question(target_path = destination_target_path,
                                                        target_is_source = True,
                                                        command = args.command)
                force_diffuse = utils.prompt_question(question = question, default = 'y')
                if force_diffuse:
                    utils.remove(path = source_target_path)
                    diffuse_dotfile(source_target_path = source_target_path,
                                    destination_target_path = destination_target_path)


def add(args: Namespace) -> None:
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')

    target = args.target
    if not os.path.exists(target):
        raise OSError(f"Target {target} not found.")

    config = utils.read_map_file(map_file_path = map_file_path)
    current_targets = []
    if os.path.isfile(target):
        current_targets = config['Targets']['files'].split()
    elif os.path.isdir(target):
        current_targets = config['Targets']['directories'].split()

    relative_target_path = os.path.expanduser(target).replace(os.path.expanduser(config['Paths']['source']), '')[1:]
    if relative_target_path in current_targets:
        print(f"Target {target} already in map file.")
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
        print(f"Target {target} not found in map file")

    utils.write_map_file(map_file_path = map_file_path, config = config)


def link_dotfile(source_target_path: str, destination_target_path: str, backup: bool) -> None:
    if backup:
        utils.copy(source = source_target_path, destination = destination_target_path)
        backup_path = utils.generate_backup_path(path = source_target_path)
        os.rename(source_target_path, backup_path)
    else:
        if not os.path.exists(os.path.dirname(destination_target_path)):
            os.makedirs(os.path.dirname(destination_target_path))
        shutil.move(source_target_path, destination_target_path)
    os.symlink(destination_target_path, source_target_path)


def unlink_dotfile(source_target_path: str, destination_target_path: str, source: str, destination: str) -> None:
    utils.remove(path = source_target_path)
    shutil.move(destination_target_path, source_target_path)
    backup_path = utils.generate_backup_path(path = source_target_path)
    utils.remove(path = backup_path)

    parent_directory = os.path.dirname(destination_target_path)
    while (parent_directory != source) and (parent_directory != destination):
        if not os.listdir(parent_directory):
            shutil.rmtree(parent_directory)
            parent_directory = os.path.dirname(parent_directory)
        else:
            break


def diffuse_dotfile(source_target_path: str, destination_target_path: str) -> None:
    os.symlink(destination_target_path, source_target_path)
