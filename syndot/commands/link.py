from argparse import Namespace
import os
import shutil
from syndot import utils
from .diffuse import diffuse_dotfile


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


def link_dotfile(settings_dir: str, system_target_path: str, settings_target_path: str, backup: bool) -> None:
    utils.copy(source = system_target_path, destination = settings_target_path)
    utils.change_parent_owner(source = system_target_path, destination = settings_target_path,
                              settings_dir = settings_dir)
    if os.path.isdir(system_target_path):
        utils.change_child_owner(source = system_target_path, destination = settings_target_path)
    if backup:
        backup_path = utils.generate_backup_path(path = system_target_path)
        os.rename(system_target_path, backup_path)
    else:
        utils.remove(system_target_path)
    os.symlink(settings_target_path, system_target_path)
