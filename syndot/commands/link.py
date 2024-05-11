from argparse import Namespace
import os
from syndot import utils
from syndot.commands.utils import skip_dotfiles


def link(args: Namespace) -> None:
    settings_dir, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile), args = args)

    targets_to_be_linked = {}
    already_existing_settings = {}
    missing_system_targets = []
    already_linked_targets = []
    corrupted_targets = []
    wrong_existing_links = []

    for target in targets:
        system_target_path, settings_target_path = utils.compose_target_paths(settings_dir = settings_dir,
                                                                              target = target)

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

    link_dotfiles(targets_list = targets_to_be_linked,
                  settings_dir = settings_dir,
                  backup = args.backup,
                  many_targets_sentence = f"Found {len(targets_to_be_linked.keys())} files or directories to be "
                                          f"linked:",
                  many_targets_question = "\nDo you want to proceed to link the above listed files and directories "
                                          "(y/N)? ",
                  single_file_sentence = f"Found {len(targets_to_be_linked.keys())} file to be linked:",
                  single_file_question = "\nDo you want to proceed to link this file (y/N)? ",
                  single_directory_sentence = f"Found {len(targets_to_be_linked.keys())} directory to be linked:",
                  single_directory_question = "\nDo you want to proceed to link this directory (y/N)? ",
                  remove_settings = False)

    link_dotfiles(targets_list = already_existing_settings,
                  settings_dir = settings_dir,
                  backup = args.backup,
                  many_targets_sentence = f"Found {len(already_existing_settings.keys())} already existing files or "
                                          f"directories in settings directory:",
                  many_targets_question = "\nDo you want to remove the files and directory from settings directory and "
                                          "proceed to link the correspondent ones (y/N)? ",
                  single_file_sentence = f"Found {len(already_existing_settings.keys())} already existing file in "
                                         f"settings directory:",
                  single_file_question = "\nDo you want to remove this file from settings directory and proceed to "
                                         "link the correspondent one (y/N)? ",
                  single_directory_sentence = f"Found {len(already_existing_settings.keys())} already existing "
                                              f"directory in settings directory:",
                  single_directory_question = "\nDo you want to remove this directory from settings directory and "
                                              "proceed to link the correspondent one (y/N)? ",
                  remove_settings = True)

    skip_dotfiles(targets_list = missing_system_targets,
                  many_targets_sentence = f"Skipping {len(missing_system_targets)} missing files or directories:",
                  single_file_sentence = f"Skipping {len(missing_system_targets)} missing file:",
                  single_directory_sentence = f"Skipping {len(missing_system_targets)} missing directory:")

    skip_dotfiles(targets_list = already_linked_targets,
                  many_targets_sentence = f"Skipping {len(already_linked_targets)} already linked files or "
                                          f"directories:",
                  single_file_sentence = f"Skipping {len(already_linked_targets)} already linked file:",
                  single_directory_sentence = f"Skipping {len(already_linked_targets)} already linked directory:")

    skip_dotfiles(targets_list = corrupted_targets,
                  many_targets_sentence = f"Skipping {len(corrupted_targets)} files or directories because are links "
                                          f"to non-existing files or directories:",
                  single_file_sentence = f"Skipping {len(corrupted_targets)} file because is a link to a non-existing "
                                         f"file:",
                  single_directory_sentence = f"Skipping {len(corrupted_targets)} directory because is a link to a "
                                              f"non-existing directory:")

    skip_dotfiles(targets_list = wrong_existing_links,
                  many_targets_sentence = f"Skipping {len(wrong_existing_links)} files or directories because are "
                                          f"links to wrong existing files or directories:",
                  single_file_sentence = f"Skipping {len(wrong_existing_links)} file because is a link to a wrong "
                                         f"existing file:",
                  single_directory_sentence = f"Skipping {len(wrong_existing_links)} directory because is a link to a "
                                              f"wrong existing directory:")


def link_dotfiles(targets_list: dict[str, str],
                  settings_dir: str,
                  backup: bool,
                  many_targets_sentence: str,
                  many_targets_question: str,
                  single_file_sentence: str,
                  single_file_question: str,
                  single_directory_sentence: str,
                  single_directory_question: str,
                  remove_settings: bool) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())
        if n_targets > 1:
            print(many_targets_sentence)
            for system_target_path, settings_target_path in targets_list.items():
                utils.print_relationship(system_target_path = system_target_path,
                                         settings_target_path = settings_target_path,
                                         symbol = '-->')
            proceed = utils.ask_to_proceed(question = many_targets_question)
        else:
            if os.path.isfile(list(targets_list.keys())[0]):
                print(single_file_sentence)
                utils.print_relationship(system_target_path = list(targets_list.keys())[0],
                                         settings_target_path = list(targets_list.values())[0],
                                         symbol = '-->')
                proceed = utils.ask_to_proceed(question = single_file_question)
            else:
                print(single_directory_sentence)
                utils.print_relationship(system_target_path = list(targets_list.keys())[0],
                                         settings_target_path = list(targets_list.values())[0],
                                         symbol = '-->')
                proceed = utils.ask_to_proceed(question = single_directory_question)

        if proceed:
            for i, (system_target_path, settings_target_path) in enumerate(targets_list.items(), 1):
                utils.print_action(action_type = 'link',
                                   system_target_path = system_target_path,
                                   settings_target_path = settings_target_path)
                print(f"Total ({i}/{n_targets})", end = '\r')

                if remove_settings:
                    utils.remove(path = settings_target_path)
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
        print()
