from argparse import Namespace
import os
from syndot import utils
from syndot.commands.utils import skip_dotfiles


def diffuse(args: Namespace) -> None:
    settings_dir, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile), args = args)

    targets_to_be_diffused = {}
    already_existing_system = {}
    already_diffused_targets = []
    wrong_existing_links = {}
    missing_settings_targets = []
    settings_are_links = []

    for target in targets:
        system_target_path, settings_target_path = utils.compose_target_paths(settings_dir = settings_dir,
                                                                              target = target)
        if not os.path.islink(settings_target_path):
            if os.path.exists(settings_target_path):
                if not os.path.islink(system_target_path):
                    if not os.path.exists(system_target_path):
                        targets_to_be_diffused[system_target_path] = settings_target_path
                    else:
                        already_existing_system[system_target_path] = settings_target_path
                else:
                    if os.readlink(system_target_path) == settings_target_path:
                        already_diffused_targets.append(system_target_path)
                    else:
                        wrong_existing_links[system_target_path] = settings_target_path
            else:
                missing_settings_targets.append(settings_target_path)
        else:
            settings_are_links.append(settings_target_path)

    diffuse_dotfiles(targets_list = targets_to_be_diffused,
                     many_targets_sentence = f"Found {len(targets_to_be_diffused.keys())} files or directories to be "
                                             f"diffused:",
                     many_targets_question = "\nDo you want to proceed to diffuse the above listed files and "
                                             "directories (y/N)? ",
                     single_file_sentence = f"Found {len(targets_to_be_diffused.keys())} file to be diffused:",
                     single_file_question = "\nDo you want to proceed to diffuse this file (y/N)? ",
                     single_directory_sentence = f"Found {len(targets_to_be_diffused.keys())} directory to be "
                                                 f"diffused:",
                     single_directory_question = "\nDo you want to proceed to diffuse this directory (y/N)? ",
                     remove_system = False)

    diffuse_dotfiles(targets_list = already_existing_system,
                     many_targets_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                             f"files or directories:",
                     many_targets_question = "\nDo you want to proceed to diffuse the above listed files and "
                                             "directories (y/N)? ",
                     single_file_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                            f"file:",
                     single_file_question = "\nDo you want to proceed to diffuse this file (y/N)? ",
                     single_directory_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                                 f"directory:",
                     single_directory_question = "\nDo you want to proceed to diffuse this directory (y/N)? ",
                     remove_system = True)

    diffuse_dotfiles(targets_list = wrong_existing_links,
                     many_targets_sentence = f"Found {len(wrong_existing_links.keys())} files or directories that are "
                                             f"links to wrong files or directories:",
                     many_targets_question = "\nDo you want to proceed to diffuse the above listed files and "
                                             "directories (y/N)? ",
                     single_file_sentence = f"Found {len(wrong_existing_links.keys())} file that is a link to a wrong "
                                            f"file:",
                     single_file_question = "\nDo you want to proceed to diffuse this file (y/N)? ",
                     single_directory_sentence = f"Found {len(wrong_existing_links.keys())} directory that is a link "
                                                 f"to a wrong directory:",
                     single_directory_question = "\nDo you want to proceed to diffuse this directory (y/N)? ",
                     remove_system = True)

    skip_dotfiles(targets_list = already_diffused_targets,
                  many_targets_sentence = f"Skipping {len(already_diffused_targets)} already diffused files or "
                                          f"directories:",
                  single_file_sentence = f"Skipping {len(already_diffused_targets)} already diffused file:",
                  single_directory_sentence = f"Skipping {len(already_diffused_targets)} already diffused directory:")

    skip_dotfiles(targets_list = missing_settings_targets,
                  many_targets_sentence = f"Skipping {len(missing_settings_targets)} missing settings files or "
                                          f"directories:",
                  single_file_sentence = f"Skipping {len(missing_settings_targets)} missing settings file:",
                  single_directory_sentence = f"Skipping {len(missing_settings_targets)} missing settings directory:")

    skip_dotfiles(targets_list = settings_are_links,
                  many_targets_sentence = f"Skipping {len(settings_are_links)} settings files or directories because "
                                          f"are links:",
                  single_file_sentence = f"Skipping {len(settings_are_links)} settings file because is a link:",
                  single_directory_sentence = f"Skipping {len(settings_are_links)} settings directory because is a "
                                              f"link:")


def diffuse_dotfiles(targets_list: dict[str, str],
                     many_targets_sentence: str,
                     many_targets_question: str,
                     single_file_sentence: str,
                     single_file_question: str,
                     single_directory_sentence: str,
                     single_directory_question: str,
                     remove_system: bool) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())
        if n_targets > 1:
            print(many_targets_sentence)
            for system_target_path, settings_target_path in targets_list.items():
                utils.print_relationship(system_target_path = system_target_path,
                                         settings_target_path = settings_target_path,
                                         symbol = '<--')
            proceed = utils.ask_to_proceed(question = many_targets_question)
        else:
            if os.path.isfile(list(targets_list.keys())[0]):
                print(single_file_sentence)
                utils.print_relationship(system_target_path = list(targets_list.keys())[0],
                                         settings_target_path = list(targets_list.values())[0],
                                         symbol = '<--')
                proceed = utils.ask_to_proceed(question = single_file_question)
            else:
                print(single_directory_sentence)
                utils.print_relationship(system_target_path = list(targets_list.keys())[0],
                                         settings_target_path = list(targets_list.values())[0],
                                         symbol = '<--')
                proceed = utils.ask_to_proceed(question = single_directory_question)

        if proceed:
            for i, (system_target_path, settings_target_path) in enumerate(targets_list.items(), 1):
                utils.print_action(action_type = 'diffuse',
                                   system_target_path = system_target_path,
                                   settings_target_path = settings_target_path)
                print(f"Total ({i}/{n_targets})", end = '\r')

                if remove_system:
                    utils.remove(system_target_path)
                if not os.path.exists(os.path.dirname(system_target_path)):
                    os.makedirs(os.path.dirname(system_target_path))
                os.symlink(settings_target_path, system_target_path)
        print()
