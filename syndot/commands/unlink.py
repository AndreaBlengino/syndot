from argparse import Namespace
import os
import shutil
from syndot import utils


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
