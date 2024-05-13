from argparse import Namespace
import os
import shutil
from syndot.utils.commands import skip_dotfiles
from syndot.utils.file_actions import remove
from syndot.utils.map_file import get_map_info, read_map_file
from syndot.utils.path import compose_target_paths, expand_home_path, generate_backup_path
from syndot.utils.print_ import print_action, print_highlight, print_relationship
from syndot.utils.prompt import ask_to_proceed


def unlink(args: Namespace) -> None:
    settings_dir, targets = get_map_info(config = read_map_file(map_file_path = args.mapfile), args = args)

    targets_to_be_unlinked = {}
    wrong_existing_links = {}
    already_existing_system = {}
    already_unlinked_targets = []
    missing_settings_targets = []
    settings_are_links = []

    print_highlight('Looking for files and directories to unlink...')

    for target in targets:
        system_target_path, settings_target_path = compose_target_paths(settings_dir = settings_dir, target = target)

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

    if not any([targets_to_be_unlinked, wrong_existing_links, already_existing_system, already_unlinked_targets,
                missing_settings_targets, settings_are_links]):
        print_highlight('No files or directories found to unlink.')

    unlink_dotfiles(targets_list = targets_to_be_unlinked,
                    settings_dir = settings_dir,
                    many_targets_sentence = f"Found {len(targets_to_be_unlinked.keys())} files or directories to "
                                            f"unlink.\nThey will be moved to the respective system directories.\nThe "
                                            f"original symbolic links and eventually the backups will be removed.",
                    single_file_sentence = f"Found {len(targets_to_be_unlinked.keys())} file to unlink.\nIt will be "
                                           f"moved to the respective system directory.\nThe original symbolic link and"
                                           f"eventually the backup file will be removed.",
                    single_directory_sentence = f"Found {len(targets_to_be_unlinked.keys())} directory to unlinked.\n"
                                                f"It will be moved to the respective system directory.\nThe original "
                                                f"symbolic link and eventually the backup directory will be removed.")

    unlink_dotfiles(targets_list = wrong_existing_links,
                    settings_dir = settings_dir,
                    many_targets_sentence = f"Found {len(wrong_existing_links.keys())} files or directories that are "
                                            f"links to wrong files or directories.\nThese wrong links will be removed"
                                            f"and eventually also the backups.\nThen the settings files and directories"
                                            f"will be moved to the respective system directories.",
                    single_file_sentence = f"Found {len(wrong_existing_links.keys())} file that is a link to a wrong "
                                           f"file.\nThis wrong link will be removed and eventually also the backup "
                                           f"file.\nThen the settings file will be moved to the respective system "
                                           f"directory.",
                    single_directory_sentence = f"Found {len(wrong_existing_links.keys())} directory that is a link to "
                                                f"a wrong directory.\nThis wrong link will be removed and eventually "
                                                f"also the backup directory.\nThen the settings directory will be "
                                                f"moved to the respective system directory.")

    unlink_dotfiles(targets_list = already_existing_system,
                    settings_dir = settings_dir,
                    many_targets_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                            f"files or directories.\nThey will be removed and eventually also the "
                                            f"backups.\nThen the settings files and directories will be moved to the "
                                            f"respective system directories.",
                    single_file_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                           f"file.\nIt will be removed and eventually also the backup file.\nThen the "
                                           f"settings file will be moved to the respective system directory.",
                    single_directory_sentence = f"Found {len(already_existing_system.keys())} already existing system "
                                                f"directory.\nIt will be removed and eventually also the backup "
                                                f"directory.\nThen the settings directory will be moved to the "
                                                f"respective system directory.")

    skip_dotfiles(targets_list = already_unlinked_targets,
                  many_targets_sentence = f"Skipping {len(already_unlinked_targets)} already unlinked files or "
                                          f"directories.",
                  single_file_sentence = f"Skipping {len(already_unlinked_targets)} already unlinked file.",
                  single_directory_sentence = f"Skipping {len(already_unlinked_targets)} already unlinked directory.")

    skip_dotfiles(targets_list = missing_settings_targets,
                  many_targets_sentence = f"Skipping {len(missing_settings_targets)} missing settings files or "
                                          f"directories.",
                  single_file_sentence = f"Skipping {len(missing_settings_targets)} missing settings file.",
                  single_directory_sentence = f"Skipping {len(missing_settings_targets)} missing settings directory.")

    skip_dotfiles(targets_list = settings_are_links,
                  many_targets_sentence = f"Skipping {len(settings_are_links)} settings files or directories because "
                                          f"are links.",
                  single_file_sentence = f"Skipping {len(settings_are_links)} settings file because is a link.",
                  single_directory_sentence = f"Skipping {len(settings_are_links)} settings directory because is a "
                                              f"link.")


def unlink_dotfiles(targets_list: dict[str, str],
                    settings_dir: str,
                    many_targets_sentence: str,
                    single_file_sentence: str,
                    single_directory_sentence: str) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())
        if n_targets > 1:
            for system_target_path, settings_target_path in targets_list.items():
                print_relationship(system_target_path = system_target_path,
                                   settings_target_path = settings_target_path,
                                   symbol = '-x->')
            print_highlight(many_targets_sentence)
            proceed = ask_to_proceed()
        else:
            if os.path.isfile(list(targets_list.keys())[0]):
                print_relationship(system_target_path = list(targets_list.keys())[0],
                                   settings_target_path = list(targets_list.values())[0],
                                   symbol = '-x->')
                print_highlight(single_file_sentence)
                proceed = ask_to_proceed()
            else:
                print_relationship(system_target_path = list(targets_list.keys())[0],
                                   settings_target_path = list(targets_list.values())[0],
                                   symbol = '-x->')
                print_highlight(single_directory_sentence)
                proceed = ask_to_proceed()

        if proceed:
            for i, (system_target_path, settings_target_path) in enumerate(targets_list.items(), 1):
                print_action(action_type = 'unlink',
                             system_target_path = system_target_path,
                             settings_target_path = settings_target_path)
                print(f"Total ({i}/{n_targets})", end = '\r')

                remove(path = system_target_path)
                shutil.move(settings_target_path, system_target_path)
                backup_path = generate_backup_path(path = system_target_path)
                remove(path = backup_path)

                parent_directory = os.path.dirname(settings_target_path)
                protected_directories = (settings_dir, expand_home_path('~'), '/')
                while parent_directory not in protected_directories:
                    parent_directory_content = os.listdir(parent_directory)
                    if not parent_directory_content or ((len(parent_directory_content) == 1) and
                                                        parent_directory_content[0] == '.directory'):
                        shutil.rmtree(parent_directory)
                        parent_directory = os.path.dirname(parent_directory)
                    else:
                        break
        print()
