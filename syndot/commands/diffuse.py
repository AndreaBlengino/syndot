from argparse import Namespace
import os
from syndot.init_config import LOG_FILE_PATH
from syndot.utils.commands import skip_dotfiles
from syndot.utils.file_actions import remove
from syndot.utils.logger import log_error
from syndot.utils.map_file import get_map_info, read_map_file
from syndot.utils.path import compose_target_paths
from syndot.utils.print_ import print_action, print_error, print_highlight, print_relationship
from syndot.utils.prompt import ask_to_proceed


def diffuse(args: Namespace) -> None:
    settings_dir, targets = get_map_info(config = read_map_file(map_file_path = args.mapfile), args = args)

    targets_to_be_diffused = {}
    already_existing_system = {}
    already_diffused_targets = []
    wrong_existing_links = {}
    missing_settings_targets = []
    settings_are_links = []

    print_highlight('Looking for files and directories to diffuse...')

    for target in targets:
        system_target_path, settings_target_path = compose_target_paths(settings_dir = settings_dir, target = target)
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

    if not any([targets_to_be_diffused, already_existing_system, already_diffused_targets, wrong_existing_links,
                missing_settings_targets, settings_are_links]):
        print_highlight('No files or directories found to diffuse.')

    diffuse_dotfiles(targets_list = targets_to_be_diffused,
                     many_targets_sentence = f"Found {len(targets_to_be_diffused.keys())} files or directories to "
                                             f"diffuse.\nSymbolic links to these settings files and directories will "
                                             f"be created in the respective system directories.",
                     single_file_sentence = f"Found {len(targets_to_be_diffused.keys())} file to diffuse.\nA symbolic "
                                            f"link to this file will be created in the respective system directory.",
                     single_directory_sentence = f"Found {len(targets_to_be_diffused.keys())} directory to diffuse.\n"
                                                 f"A symbolic link to this directory will be created in the respective "
                                                 f"system directory.",
                     remove_system = False)

    diffuse_dotfiles(targets_list = already_existing_system,
                     many_targets_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                             f"files or directories.\nThey will be removed and replaced by symbolic "
                                             f"links to the respective files and directories in the settings "
                                             f"directory.",
                     single_file_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                            f"file.\nIt will be removed and replaced by a symbolic link to the "
                                            f"respective file in the settings directory.",
                     single_directory_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                                 f"directory.\nIt will be removed and replaced by a symbolic link to "
                                                 f"the respective directory in the settings directory.",
                     remove_system = True)

    diffuse_dotfiles(targets_list = wrong_existing_links,
                     many_targets_sentence = f"Found {len(wrong_existing_links.keys())} files or directories that are "
                                             f"links to wrong files or directories.\nThey will be removed and replaced "
                                             f"by symbolic links to the respective files and directories in the "
                                             f"settings directory.",
                     single_file_sentence = f"Found {len(wrong_existing_links.keys())} file that is a link to a wrong "
                                            f"file.\nIt will be removed and replaced by a symbolic link to the "
                                            f"respective file in the settings directory.",
                     single_directory_sentence = f"Found {len(wrong_existing_links.keys())} directory that is a link "
                                                 f"to a wrong directory.\nIt will be removed and replaced by a "
                                                 f"symbolic link to the respective directory in the settings "
                                                 f"directory.",
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
                     single_file_sentence: str,
                     single_directory_sentence: str,
                     remove_system: bool) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())
        if n_targets > 1:
            for system_target_path, settings_target_path in targets_list.items():
                print_relationship(system_target_path = system_target_path,
                                   settings_target_path = settings_target_path,
                                   symbol = '<--')
            print_highlight(many_targets_sentence)
            proceed = ask_to_proceed()
        else:
            if os.path.isfile(list(targets_list.values())[0]):
                print_relationship(system_target_path = list(targets_list.keys())[0],
                                   settings_target_path = list(targets_list.values())[0],
                                   symbol = '<--')
                print_highlight(single_file_sentence)
                proceed = ask_to_proceed()
            else:
                print_relationship(system_target_path = list(targets_list.keys())[0],
                                   settings_target_path = list(targets_list.values())[0],
                                   symbol = '<--')
                print_highlight(single_directory_sentence)
                proceed = ask_to_proceed()

        if proceed:
            for i, (system_target_path, settings_target_path) in enumerate(targets_list.items(), 1):
                try:
                    print_action(action_type = 'diffuse',
                                 system_target_path = system_target_path,
                                 settings_target_path = settings_target_path)
                    print(f"Total ({i}/{n_targets})", end = '\r')

                    if remove_system:
                        remove(system_target_path)
                    if not os.path.exists(os.path.dirname(system_target_path)):
                        os.makedirs(os.path.dirname(system_target_path))
                    os.symlink(settings_target_path, system_target_path)
                except Exception as e:
                    print_error(f"Error in diffusing {system_target_path}. Check {LOG_FILE_PATH} for more details.")
                    log_error(f'{e}')
        print('\n')
