from argparse import Namespace
import os
from syndot import utils


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


def diffuse_dotfile(system_target_path: str, settings_target_path: str) -> None:
    if not os.path.exists(os.path.dirname(system_target_path)):
        os.makedirs(os.path.dirname(system_target_path))
    os.symlink(settings_target_path, system_target_path)
