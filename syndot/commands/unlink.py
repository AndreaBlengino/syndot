from argparse import Namespace
import os
import shutil
from syndot import utils
from syndot.commands.utils import skip_dotfiles


def unlink(args: Namespace) -> None:
    settings_dir, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile),
                                               target = args.target)

    targets_to_be_unlinked = {}
    wrong_existing_links = {}
    already_existing_system = {}
    already_unlinked_targets = []
    missing_settings_targets = []
    settings_are_links = []

    for target in targets:
        system_target_path, settings_target_path = utils.compose_target_paths(settings_dir = settings_dir,
                                                                              target = target)

        if not os.path.islink(settings_target_path):
            if os.path.exists(settings_target_path):
                if os.path.islink(system_target_path):
                    if os.readlink(system_target_path) == settings_target_path:
                        targets_to_be_unlinked[system_target_path] = settings_target_path
                    else:
                        wrong_existing_links[system_target_path] = settings_target_path
                else:
                    if not os.path.exists(system_target_path):
                        targets_to_be_unlinked[system_target_path] = settings_target_path
                    else:
                        already_existing_system[system_target_path] = settings_target_path
            else:
                if os.path.exists(system_target_path):
                    already_unlinked_targets.append(settings_target_path)
                else:
                    missing_settings_targets.append(settings_target_path)
        else:
            settings_are_links.append(settings_target_path)

    unlink_dotfiles(targets_list = targets_to_be_unlinked,
                    settings_dir = settings_dir,
                    many_targets_sentence = f"Found {len(targets_to_be_unlinked.keys())} files or directories to be "
                                            f"unlinked:",
                    many_targets_question = "\nDo you want to proceed to unlink the above listed files and directories "
                                            "(y/N)? ",
                    single_file_sentence = f"Found {len(targets_to_be_unlinked.keys())} file to be unlinked:",
                    single_file_question = "\nDo you want to proceed to unlink this file (y/N)? ",
                    single_directory_sentence = f"Found {len(targets_to_be_unlinked.keys())} directory to be unlinked:",
                    single_directory_question = "\nDo you want to proceed to unlink this directory (y/N)? ")

    unlink_dotfiles(targets_list = wrong_existing_links,
                    settings_dir = settings_dir,
                    many_targets_sentence = f"Found {len(wrong_existing_links.keys())} files or directories that are "
                                            f"links to wrong files or directories:",
                    many_targets_question = "\nDo you want to proceed to unlink the above listed files and directories "
                                            "(y/N)? ",
                    single_file_sentence = f"Found {len(wrong_existing_links.keys())} file that is a link to a wrong "
                                           f"file:",
                    single_file_question = "\nDo you want to proceed to unlink this file (y/N)? ",
                    single_directory_sentence = f"Found {len(wrong_existing_links.keys())} directory that is a link to "
                                                f"a wrong directory:",
                    single_directory_question = "\nDo you want to proceed to unlink this directory (y/N)? ")

    unlink_dotfiles(targets_list = already_existing_system,
                    settings_dir = settings_dir,
                    many_targets_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                            f"files or directories:",
                    many_targets_question = "\nDo you want to proceed to unlink the above listed files and directories "
                                            "(y/N)? ",
                    single_file_sentence = f"Found {len(already_existing_system.keys())} already existing system file:",
                    single_file_question = "\nDo you want to proceed to unlink this file (y/N)? ",
                    single_directory_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                                f"directory:",
                    single_directory_question = "\nDo you want to proceed to unlink this directory (y/N)? ")

    skip_dotfiles(targets_list = already_unlinked_targets,
                  many_targets_sentence = f"Skipping {len(already_unlinked_targets)} already unlinked files or "
                                          f"directories:",
                  single_file_sentence = f"Skipping {len(already_unlinked_targets)} already unlinked file:",
                  single_directory_sentence = f"Skipping {len(already_unlinked_targets)} already unlinked directory:")

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


def unlink_dotfiles(targets_list: dict[str, str],
                    settings_dir: str,
                    many_targets_sentence: str,
                    many_targets_question: str,
                    single_file_sentence: str,
                    single_file_question: str,
                    single_directory_sentence: str,
                    single_directory_question: str) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())
        if n_targets > 1:
            print(many_targets_sentence)
            for system_target_path, settings_target_path in targets_list.items():
                print(f"{system_target_path} -x-> {settings_target_path}")
            proceed = utils.ask_to_proceed(question = many_targets_question)
        else:
            if os.path.isfile(list(targets_list.keys())[0]):
                print(single_file_sentence)
                print(f"{list(targets_list.keys())[0]} -x-> {list(targets_list.values())[0]}")
                proceed = utils.ask_to_proceed(question = single_file_question)
            else:
                print(single_directory_sentence)
                print(f"{list(targets_list.keys())[0]} -x-> {list(targets_list.values())[0]}")
                proceed = utils.ask_to_proceed(question = single_directory_question)

        if proceed:
            for i, (system_target_path, settings_target_path) in enumerate(targets_list.items(), 1):
                print(f"Unlinking {system_target_path} from {settings_target_path}")
                print(f"Total ({i}/{n_targets})", end = '\r')

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
        print()
