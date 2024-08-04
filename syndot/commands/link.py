from argparse import Namespace
import os
from syndot.init_config import LOG_FILE_PATH
from syndot.utils.commands import skip_dotfiles, print_dotfiles_to_manage
from syndot.utils.file_actions import (
    change_parent_owner,
    change_child_owner,
    copy,
    remove
)
from syndot.utils.logger import log_error
from syndot.utils.map_file import get_map_info, read_map_file
from syndot.utils.path import compose_target_paths, generate_backup_path
from syndot.utils.print_ import (
    print_action,
    print_error,
    print_highlight
)
from syndot.utils.prompt import ask_to_proceed


def link(args: Namespace) -> None:
    settings_dir, targets = get_map_info(
        config=read_map_file(map_file_path=args.mapfile),
        args=args
    )

    targets_to_be_linked = {}
    already_existing_settings = {}
    missing_system_targets = []
    already_linked_targets = []
    corrupted_targets = []
    wrong_existing_links = []

    print_highlight("Looking for files and directories to link...")

    for target in targets:
        system_target_path, settings_target_path = compose_target_paths(
            settings_dir=settings_dir,
            target=target
        )

        if _check_tartgets_to_be_linked(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            targets_to_be_linked[system_target_path] = settings_target_path

        if _check_already_existing_settings(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            already_existing_settings[system_target_path] = \
                settings_target_path

        if _check_missing_system_targets(
            system_target_path=system_target_path
        ):
            missing_system_targets.append(system_target_path)

        if _check_already_linked_targets(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            already_linked_targets.append(system_target_path)

        if _check_corrupted_targets(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            corrupted_targets.append(system_target_path)

        if _check_wrong_existing_links(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            wrong_existing_links.append(system_target_path)

    if not any([
        targets_to_be_linked,
        already_existing_settings,
        missing_system_targets,
        already_linked_targets,
        corrupted_targets,
        wrong_existing_links
    ]):
        print_highlight("No files or directories found to link.")

    link_dotfiles(
        targets_list=targets_to_be_linked,
        settings_dir=settings_dir,
        backup=args.backup,
        many_targets_sentence=f"Found {len(targets_to_be_linked.keys())} "
                              f"files or directories to link.\nThey will be "
                              f"moved to settings directory and will be "
                              f"replaced by symbolic links.",
        single_file_sentence=f"Found {len(targets_to_be_linked.keys())} file "
                             f"to link.\nIt will be moved to settings "
                             f"directory and will be replaced by a symbolic "
                             f"link.",
        single_directory_sentence=f"Found {len(targets_to_be_linked.keys())} "
                                  f"directory to link.\nIt will be moved to "
                                  f"settings directory and will be replaced "
                                  f"by a symbolic link.",
        remove_settings=False,
        ask_for_confirmation=not args.no_confirm
    )

    link_dotfiles(
        targets_list=already_existing_settings,
        settings_dir=settings_dir,
        backup=args.backup,
        many_targets_sentence=f"Found {len(already_existing_settings.keys())} "
                              f"already existing files or directories in "
                              f"settings directory.\nThey will be removed, "
                              f"then the respective files and directories "
                              f"from the system will be moved to settings "
                              f"directory and will be replaced by symbolic "
                              f"links.",
        single_file_sentence=f"Found {len(already_existing_settings.keys())} "
                             f"already existing file in settings directory.\n"
                             f"It will be removed, then the respective file "
                             f"from the system will be moved to settings "
                             f"directory and will be replaced by a symbolic "
                             f"link.",
        single_directory_sentence=f"Found "
                                  f"{len(already_existing_settings.keys())} "
                                  f"already existing directory in settings "
                                  f"directory.\nIt will be removed, then the "
                                  f"respective directory from the system will "
                                  f"be moved to settings directory and will "
                                  f"be replaced by a symbolic link.",
        remove_settings=True,
        ask_for_confirmation=not args.no_confirm
    )

    skip_dotfiles(
        targets_list=missing_system_targets,
        many_targets_sentence=f"Skipping {len(missing_system_targets)} "
                              f"missing files or directories.",
        single_file_sentence=f"Skipping {len(missing_system_targets)} "
                             f"missing file.",
        single_directory_sentence=f"Skipping {len(missing_system_targets)} "
                                  f"missing directory."
    )

    skip_dotfiles(
        targets_list=already_linked_targets,
        many_targets_sentence=f"Skipping {len(already_linked_targets)} "
                              f"already linked files or directories.",
        single_file_sentence=f"Skipping {len(already_linked_targets)} "
                             f"already linked file.",
        single_directory_sentence=f"Skipping {len(already_linked_targets)} "
                                  f"already linked directory."
    )

    skip_dotfiles(
        targets_list=corrupted_targets,
        many_targets_sentence=f"Skipping {len(corrupted_targets)} files or "
                              f"directories because are links to non-existing "
                              f"files or directories.",
        single_file_sentence=f"Skipping {len(corrupted_targets)} file because "
                             f"is a link to a non-existing file.",
        single_directory_sentence=f"Skipping {len(corrupted_targets)} "
                                  f"directory because is a link to a "
                                  f"non-existing directory."
    )

    skip_dotfiles(
        targets_list=wrong_existing_links,
        many_targets_sentence=f"Skipping {len(wrong_existing_links)} files "
                              f"or directories because are links to wrong "
                              f"existing files or directories.",
        single_file_sentence=f"Skipping {len(wrong_existing_links)} file "
                             f"because is a link to a wrong existing file.",
        single_directory_sentence=f"Skipping {len(wrong_existing_links)} "
                                  f"directory because is a link to a wrong "
                                  f"existing directory."
    )


def link_dotfiles(
    targets_list: dict[str, str],
    settings_dir: str,
    backup: bool,
    many_targets_sentence: str,
    single_file_sentence: str,
    single_directory_sentence: str,
    remove_settings: bool,
    ask_for_confirmation: bool
) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())

        print_dotfiles_to_manage(
            targets_list=targets_list,
            many_targets_sentence=many_targets_sentence,
            single_file_sentence=single_directory_sentence,
            single_directory_sentence=single_directory_sentence,
            symbol='-->'
        )

        proceed = ask_to_proceed() if ask_for_confirmation else True

        if proceed:
            for i, (system_target_path, settings_target_path) in \
                    enumerate(targets_list.items(), 1):
                try:
                    print_action(
                        action_type='link',
                        system_target_path=system_target_path,
                        settings_target_path=settings_target_path
                    )
                    print(f"Total ({i}/{n_targets})", end='\r')

                    if remove_settings:
                        remove(path=settings_target_path)
                    copy(
                        source=system_target_path,
                        destination=settings_target_path
                    )
                    change_parent_owner(
                        source=system_target_path,
                        destination=settings_target_path,
                        settings_dir=settings_dir
                    )
                    if os.path.isdir(system_target_path):
                        change_child_owner(
                            source=system_target_path,
                            destination=settings_target_path
                        )
                    if backup:
                        backup_path = generate_backup_path(
                                path=system_target_path
                        )
                        os.rename(system_target_path, backup_path)
                    else:
                        remove(system_target_path)
                    os.symlink(settings_target_path, system_target_path)
                except Exception as e:
                    print_error(
                        f"Error in linking {system_target_path}. "
                        f"Check {LOG_FILE_PATH} for more details."
                    )
                    log_error(f"{e}")
        print('\n')


def _check_tartgets_to_be_linked(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(system_target_path) and \
           os.path.exists(system_target_path) and \
           not os.path.exists(settings_target_path)


def _check_already_existing_settings(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(system_target_path) and \
           os.path.exists(system_target_path) and \
           os.path.exists(settings_target_path)


def _check_missing_system_targets(system_target_path: str) -> bool:
    return not os.path.islink(system_target_path) and \
           not os.path.exists(system_target_path)


def _check_already_linked_targets(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return os.path.islink(system_target_path) and \
           (os.readlink(system_target_path) == settings_target_path) and \
           os.path.exists(system_target_path)


def _check_corrupted_targets(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return os.path.islink(system_target_path) and \
           (os.readlink(system_target_path) == settings_target_path) and \
           not os.path.exists(system_target_path)


def _check_wrong_existing_links(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return os.path.islink(system_target_path) and \
           (os.readlink(system_target_path) != settings_target_path)
