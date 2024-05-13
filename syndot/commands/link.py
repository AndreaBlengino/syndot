from argparse import Namespace
import os
from syndot.utils.commands import skip_dotfiles
from syndot.utils.file_actions import change_parent_owner, change_child_owner, copy, remove
from syndot.utils.map_file import get_map_info, read_map_file
from syndot.utils.path import compose_target_paths, generate_backup_path
from syndot.utils.print_ import print_action, print_highlight, print_relationship
from syndot.utils.prompt import ask_to_proceed


def link(args: Namespace) -> None:
    settings_dir, targets = get_map_info(config = read_map_file(map_file_path = args.mapfile), args = args)

    targets_to_be_linked = {}
    already_existing_settings = {}
    missing_system_targets = []
    already_linked_targets = []
    corrupted_targets = []
    wrong_existing_links = []

    print_highlight('Looking for files and directories to link...')

    for target in targets:
        system_target_path, settings_target_path = compose_target_paths(settings_dir = settings_dir, target = target)

        if not os.path.islink(system_target_path):
            if os.path.exists(system_target_path):
                if not os.path.exists(settings_target_path):
                    targets_to_be_linked[system_target_path] = settings_target_path
                else:
                    already_existing_settings[system_target_path] = settings_target_path
            else:
                missing_system_targets.append(system_target_path)
        else:
            if os.readlink(system_target_path) == settings_target_path:
                if os.path.exists(system_target_path):
                    already_linked_targets.append(system_target_path)
                else:
                    corrupted_targets.append(system_target_path)
            else:
                wrong_existing_links.append(system_target_path)

    if not any([targets_to_be_linked, already_existing_settings, missing_system_targets, already_linked_targets,
                corrupted_targets, wrong_existing_links]):
        print_highlight('No files or directories found to link.')

    link_dotfiles(targets_list = targets_to_be_linked,
                  settings_dir = settings_dir,
                  backup = args.backup,
                  many_targets_sentence = f"Found {len(targets_to_be_linked.keys())} files or directories to link.\n"
                                          f"They will be moved to settings directory and will be replaced by "
                                          f"symbolic links.",
                  single_file_sentence = f"Found {len(targets_to_be_linked.keys())} file to link.\nIt will be moved to "
                                         f"settings directory and will be replaced by a symbolic link.",
                  single_directory_sentence = f"Found {len(targets_to_be_linked.keys())} directory to link.\nIt will "
                                              f"be moved to settings directory and will be replaced by a symbolic "
                                              f"link.",
                  remove_settings = False)

    link_dotfiles(targets_list = already_existing_settings,
                  settings_dir = settings_dir,
                  backup = args.backup,
                  many_targets_sentence = f"Found {len(already_existing_settings.keys())} already existing files or "
                                          f"directories in settings directory.\nThey will be removed, then the "
                                          f"respective files and directories from the system will be moved to settings "
                                          f"directory and will be replaced by symbolic links.",
                  single_file_sentence = f"Found {len(already_existing_settings.keys())} already existing file in "
                                         f"settings directory.\nIt will be removed, then the respective file from the "
                                         f"system will be moved to settings directory and will be replaced by a "
                                         f"symbolic link.",
                  single_directory_sentence = f"Found {len(already_existing_settings.keys())} already existing "
                                              f"directory in settings directory.\nIt will be removed, then the "
                                              f"respective directory from the system will be moved to settings "
                                              f"directory and will be replaced by a symbolic link.",
                  remove_settings = True)

    skip_dotfiles(targets_list = missing_system_targets,
                  many_targets_sentence = f"Skipping {len(missing_system_targets)} missing files or directories.",
                  single_file_sentence = f"Skipping {len(missing_system_targets)} missing file.",
                  single_directory_sentence = f"Skipping {len(missing_system_targets)} missing directory.")

    skip_dotfiles(targets_list = already_linked_targets,
                  many_targets_sentence = f"Skipping {len(already_linked_targets)} already linked files or "
                                          f"directories.",
                  single_file_sentence = f"Skipping {len(already_linked_targets)} already linked file.",
                  single_directory_sentence = f"Skipping {len(already_linked_targets)} already linked directory.")

    skip_dotfiles(targets_list = corrupted_targets,
                  many_targets_sentence = f"Skipping {len(corrupted_targets)} files or directories because are links "
                                          f"to non-existing files or directories.",
                  single_file_sentence = f"Skipping {len(corrupted_targets)} file because is a link to a non-existing "
                                         f"file.",
                  single_directory_sentence = f"Skipping {len(corrupted_targets)} directory because is a link to a "
                                              f"non-existing directory.")

    skip_dotfiles(targets_list = wrong_existing_links,
                  many_targets_sentence = f"Skipping {len(wrong_existing_links)} files or directories because are "
                                          f"links to wrong existing files or directories.",
                  single_file_sentence = f"Skipping {len(wrong_existing_links)} file because is a link to a wrong "
                                         f"existing file.",
                  single_directory_sentence = f"Skipping {len(wrong_existing_links)} directory because is a link to a "
                                              f"wrong existing directory.")


def link_dotfiles(targets_list: dict[str, str],
                  settings_dir: str,
                  backup: bool,
                  many_targets_sentence: str,
                  single_file_sentence: str,
                  single_directory_sentence: str,
                  remove_settings: bool) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())
        if n_targets > 1:
            for system_target_path, settings_target_path in targets_list.items():
                print_relationship(system_target_path = system_target_path,
                                   settings_target_path = settings_target_path,
                                   symbol = '-->')
            print_highlight(many_targets_sentence)
            proceed = ask_to_proceed()
        else:
            if os.path.isfile(list(targets_list.keys())[0]):
                print_relationship(system_target_path = list(targets_list.keys())[0],
                                   settings_target_path = list(targets_list.values())[0],
                                   symbol = '-->')
                print_highlight(single_file_sentence)
                proceed = ask_to_proceed()
            else:
                print_relationship(system_target_path = list(targets_list.keys())[0],
                                   settings_target_path = list(targets_list.values())[0],
                                   symbol = '-->')
                print_highlight(single_directory_sentence)
                proceed = ask_to_proceed()

        if proceed:
            for i, (system_target_path, settings_target_path) in enumerate(targets_list.items(), 1):
                print_action(action_type = 'link',
                             system_target_path = system_target_path,
                             settings_target_path = settings_target_path)
                print(f"Total ({i}/{n_targets})", end = '\r')

                if remove_settings:
                    remove(path = settings_target_path)
                copy(source = system_target_path, destination = settings_target_path)
                change_parent_owner(source = system_target_path,
                                    destination = settings_target_path,
                                    settings_dir = settings_dir)
                if os.path.isdir(system_target_path):
                    change_child_owner(source = system_target_path, destination = settings_target_path)
                if backup:
                    backup_path = generate_backup_path(path = system_target_path)
                    os.rename(system_target_path, backup_path)
                else:
                    remove(system_target_path)
                os.symlink(settings_target_path, system_target_path)
        print()
