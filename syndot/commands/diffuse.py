from argparse import Namespace
import os
from syndot.init_config import LOG_FILE_PATH
from syndot.utils.commands import skip_dotfiles, print_dotfiles_to_manage
from syndot.utils.file_actions import remove
from syndot.utils.logger import log_error
from syndot.utils.map_file import get_map_info, read_map_file
from syndot.utils.path import compose_target_paths
from syndot.utils.print_ import (
    print_action,
    print_error,
    print_highlight
)
from syndot.utils.prompt import ask_to_proceed


def diffuse(args: Namespace) -> None:
    settings_dir, targets = get_map_info(
        config=read_map_file(map_file_path=args.mapfile),
        args=args
    )

    targets_to_be_diffused = {}
    already_existing_system = {}
    already_diffused_targets = []
    wrong_existing_links = {}
    missing_settings_targets = []
    settings_are_links = []

    print_highlight("Looking for files and directories to diffuse...")

    for target in targets:
        system_target_path, settings_target_path = compose_target_paths(
            settings_dir=settings_dir,
            target=target
        )

        if _check_targets_to_be_diffused(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            targets_to_be_diffused[system_target_path] = settings_target_path

        if _check_already_existing_system(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            already_existing_system[system_target_path] = settings_target_path

        if _check_already_diffused_targets(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            already_diffused_targets.append(system_target_path)

        if _check_wrong_existing_links(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            wrong_existing_links[system_target_path] = settings_target_path

        if _check_missing_settings_targets(
            settings_target_path=settings_target_path
        ):
            missing_settings_targets.append(settings_target_path)

        if _check_settings_are_links(
            settings_target_path=settings_target_path
        ):
            settings_are_links.append(settings_target_path)

    if not any([
        targets_to_be_diffused,
        already_existing_system,
        already_diffused_targets,
        wrong_existing_links,
        missing_settings_targets,
        settings_are_links
    ]):
        print_highlight("No files or directories found to diffuse.")

    diffuse_dotfiles(
        targets_list=targets_to_be_diffused,
        many_targets_sentence=f"Found {len(targets_to_be_diffused.keys())} "
                              f"files or directories to diffuse.\nSymbolic "
                              f"links to these settings files and directories "
                              f"will be created in the respective system "
                              f"directories.",
        single_file_sentence=f"Found {len(targets_to_be_diffused.keys())} "
                             f"file to diffuse.\nA symbolic link to this file "
                             f"will be created in the respective system "
                             f"directory.",
        single_directory_sentence=f"Found {len(targets_to_be_diffused.keys())}"
                                  f" directory to diffuse.\nA symbolic link "
                                  f"to this directory will be created in the "
                                  f"respective system directory.",
        remove_system=False,
        ask_for_confirmation=not args.no_confirm
    )

    diffuse_dotfiles(
        targets_list=already_existing_system,
        many_targets_sentence=f"Found {len(already_existing_system.keys())} "
                              f"already existing system files or "
                              f"directories.\nThey will be removed and "
                              f"replaced by symbolic links to the respective "
                              f"files and directories in the settings "
                              "directory.",
        single_file_sentence=f"Found {len(already_existing_system.keys())} "
                             f"already existing system file.\nIt will be "
                             f"removed and replaced by a symbolic link to the "
                             f"respective file in the settings directory.",
        single_directory_sentence=f"Found "
                                  f"{len(already_existing_system.keys())} "
                                  f"already existing system directory.\nIt "
                                  f"will be removed and replaced by a "
                                  f"symbolic link to the respective directory "
                                  f"in the settings directory.",
        remove_system=True,
        ask_for_confirmation=not args.no_confirm
    )

    diffuse_dotfiles(
        targets_list=wrong_existing_links,
        many_targets_sentence=f"Found {len(wrong_existing_links.keys())} "
                              f"files or directories that are links to wrong "
                              f"files or directories.\nThey will be removed "
                              f"and replaced by symbolic links to the "
                              f"respective files and directories in the "
                              f"settings directory.",
        single_file_sentence=f"Found {len(wrong_existing_links.keys())} file "
                             f"that is a link to a wrong file.\nIt will be "
                             f"removed and replaced by a symbolic link to the "
                             f"respective file in the settings directory.",
        single_directory_sentence=f"Found {len(wrong_existing_links.keys())} "
                                  f"directory that is a link to a wrong "
                                  f"directory.\nIt will be removed and "
                                  f"replaced by a symbolic link to the "
                                  f"respective directory in the settings "
                                  f"directory.",
        remove_system=True,
        ask_for_confirmation=not args.no_confirm
    )

    skip_dotfiles(
        targets_list=already_diffused_targets,
        many_targets_sentence=f"Skipping {len(already_diffused_targets)} "
                              f"already diffused files or directories:",
        single_file_sentence=f"Skipping {len(already_diffused_targets)} "
                             f"already diffused file:",
        single_directory_sentence=f"Skipping {len(already_diffused_targets)} "
                                  f"already diffused directory:"
    )

    skip_dotfiles(
        targets_list=missing_settings_targets,
        many_targets_sentence=f"Skipping {len(missing_settings_targets)} "
                              f"missing settings files or directories:",
        single_file_sentence=f"Skipping {len(missing_settings_targets)} "
                             f"missing settings file:",
        single_directory_sentence=f"Skipping {len(missing_settings_targets)} "
                                  f"missing settings directory:"
    )

    skip_dotfiles(
        targets_list=settings_are_links,
        many_targets_sentence=f"Skipping {len(settings_are_links)} settings "
                              f"files or directories because are links:",
        single_file_sentence=f"Skipping {len(settings_are_links)} settings "
                             f"file because is a link:",
        single_directory_sentence=f"Skipping {len(settings_are_links)} "
                                  f"settings directory because is a link:"
    )


def diffuse_dotfiles(
    targets_list: dict[str, str],
    many_targets_sentence: str,
    single_file_sentence: str,
    single_directory_sentence: str,
    remove_system: bool,
    ask_for_confirmation: bool
) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())

        print_dotfiles_to_manage(
            targets_list=targets_list,
            many_targets_sentence=many_targets_sentence,
            single_file_sentence=single_directory_sentence,
            single_directory_sentence=single_directory_sentence,
            symbol='<--'
        )

        proceed = ask_to_proceed() if ask_for_confirmation else True

        if proceed:
            for i, (system_target_path, settings_target_path) in \
                    enumerate(targets_list.items(), 1):
                try:
                    print_action(
                        action_type='diffuse',
                        system_target_path=system_target_path,
                        settings_target_path=settings_target_path
                    )
                    print(f"Total ({i}/{n_targets})", end='\r')

                    if remove_system:
                        remove(system_target_path)
                    if not os.path.exists(os.path.dirname(system_target_path)):
                        os.makedirs(os.path.dirname(system_target_path))
                    os.symlink(settings_target_path, system_target_path)
                except Exception as e:
                    print_error(
                        f"Error in diffusing {system_target_path}. "
                        f"Check {LOG_FILE_PATH} for more details."
                    )
                    log_error(f"{e}")
        print('\n')


def _check_targets_to_be_diffused(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and \
        not os.path.islink(system_target_path) and \
        not os.path.exists(system_target_path)


def _check_already_existing_system(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and \
        not os.path.islink(system_target_path) and \
        os.path.exists(system_target_path)


def _check_already_diffused_targets(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and \
        os.path.islink(system_target_path) and \
        (os.readlink(system_target_path) == settings_target_path)


def _check_wrong_existing_links(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and \
        os.path.islink(system_target_path) and \
        (os.readlink(system_target_path) != settings_target_path)


def _check_missing_settings_targets(settings_target_path: str) -> bool:
    return not os.path.islink(settings_target_path) and \
        not os.path.exists(settings_target_path)


def _check_settings_are_links(settings_target_path: str) -> bool:
    return os.path.islink(settings_target_path)
