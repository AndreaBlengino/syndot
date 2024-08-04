from argparse import Namespace
import os
import shutil
from syndot.init_config import LOG_FILE_PATH
from syndot.utils.commands import skip_dotfiles, print_dotfiles_to_manage
from syndot.utils.file_actions import remove
from syndot.utils.logger import log_error
from syndot.utils.map_file import get_map_info, read_map_file
from syndot.utils.path import (
    compose_target_paths,
    expand_home_path,
    generate_backup_path
)
from syndot.utils.print_ import (
    print_action,
    print_error,
    print_highlight
)
from syndot.utils.prompt import ask_to_proceed


def unlink(args: Namespace) -> None:
    settings_dir, targets = get_map_info(
        config=read_map_file(map_file_path=args.mapfile),
        args=args
    )

    targets_to_be_unlinked = {}
    wrong_existing_links = {}
    already_existing_system = {}
    already_unlinked_targets = []
    missing_settings_targets = []
    settings_are_links = []

    print_highlight("Looking for files and directories to unlink...")

    for target in targets:
        system_target_path, settings_target_path = compose_target_paths(
            settings_dir=settings_dir,
            target=target
        )

        if _check_targets_to_be_unlinked(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            targets_to_be_unlinked[system_target_path] = settings_target_path

        if _check_wrong_existing_links(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            wrong_existing_links[system_target_path] = settings_target_path

        if _check_already_existing_system(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            already_existing_system[system_target_path] = settings_target_path

        if _check_already_unlinked_targets(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            already_unlinked_targets.append(settings_target_path)

        if _check_missing_settings_targets(
            system_target_path=system_target_path,
            settings_target_path=settings_target_path
        ):
            missing_settings_targets.append(settings_target_path)

        if _check_settings_are_links(
            settings_target_path=settings_target_path
        ):
            settings_are_links.append(settings_target_path)

    if not any([
        targets_to_be_unlinked,
        wrong_existing_links,
        already_existing_system,
        already_unlinked_targets,
        missing_settings_targets,
        settings_are_links
    ]):
        print_highlight("No files or directories found to unlink.")

    unlink_dotfiles(
        targets_list=targets_to_be_unlinked,
        settings_dir=settings_dir,
        many_targets_sentence=f"Found {len(targets_to_be_unlinked.keys())} "
                              f"files or directories to unlink.\nThey will be "
                              f"moved to the respective system directories.\n"
                              f"The original symbolic links and eventually "
                              f"the backups will be removed.",
        single_file_sentence=f"Found {len(targets_to_be_unlinked.keys())} "
                             f"file to unlink.\nIt will be moved to the "
                             f"respective system directory.\nThe original "
                             f"symbolic link and eventually the backup file "
                             f"will be removed.",
        single_directory_sentence=f"Found {len(targets_to_be_unlinked.keys())}"
                                  f" directory to unlink.\nIt will be moved "
                                  f"to the respective system directory.\nThe "
                                  f"original symbolic link and eventually the "
                                  f"backup directory will be removed.",
        ask_for_confirmation=not args.no_confirm
    )

    unlink_dotfiles(
        targets_list=wrong_existing_links,
        settings_dir=settings_dir,
        many_targets_sentence=f"Found {len(wrong_existing_links.keys())} "
                              f"files or directories that are links to wrong "
                              f"files or directories.\nThese wrong links will "
                              f"be removed and eventually also the backups.\n"
                              f"Then the settings files and directories will "
                              f"be moved to the respective system "
                              f"directories.",
        single_file_sentence=f"Found {len(wrong_existing_links.keys())} file "
                             f"that is a link to a wrong file.\nThis wrong "
                             f"link will be removed and eventually also the "
                             f"backup file.\nThen the settings file will be "
                             f"moved to the respective system directory.",
        single_directory_sentence=f"Found {len(wrong_existing_links.keys())} "
                                  f"directory that is a link to a wrong "
                                  f"directory.\nThis wrong link will be "
                                  f"removed and eventually also the backup "
                                  f"directory.\nThen the settings directory "
                                  f"will be moved to the respective system "
                                  f"directory.",
        ask_for_confirmation=not args.no_confirm
    )

    unlink_dotfiles(
        targets_list=already_existing_system,
        settings_dir=settings_dir,
        many_targets_sentence=f"Found {len(already_existing_system.keys())} "
                              f"already existing system files or directories."
                              f"\nThey will be removed and eventually also "
                              f"the backups.\nThen the settings files and "
                              f"directories will be moved to the respective "
                              f"system directories.",
        single_file_sentence=f"Found {len(already_existing_system.keys())} "
                             f"already existing system file.\nIt will be "
                             f"removed and eventually also the backup file.\n"
                             f"Then the settings file will be moved to the "
                             f"respective system directory.",
        single_directory_sentence=f"Found "
                                  f"{len(already_existing_system.keys())} "
                                  f"already existing system directory.\nIt "
                                  f"will be removed and eventually also the "
                                  f"backup directory.\nThen the settings "
                                  f"directory will be moved to the respective "
                                  f"system directory.",
        ask_for_confirmation=not args.no_confirm
    )

    skip_dotfiles(
        targets_list=already_unlinked_targets,
        many_targets_sentence=f"Skipping {len(already_unlinked_targets)} "
                              f"already unlinked files or directories.",
        single_file_sentence=f"Skipping {len(already_unlinked_targets)} "
                             f"already unlinked file.",
        single_directory_sentence=f"Skipping {len(already_unlinked_targets)} "
                                  f"already unlinked directory."
    )

    skip_dotfiles(
        targets_list=missing_settings_targets,
        many_targets_sentence=f"Skipping {len(missing_settings_targets)} "
                              f"missing settings files or directories.",
        single_file_sentence=f"Skipping {len(missing_settings_targets)} "
                             f"missing settings file.",
        single_directory_sentence=f"Skipping {len(missing_settings_targets)} "
                                  f"missing settings directory."
    )

    skip_dotfiles(
        targets_list=settings_are_links,
        many_targets_sentence=f"Skipping {len(settings_are_links)} settings "
                              f"files or directories because are links.",
        single_file_sentence=f"Skipping {len(settings_are_links)} settings "
                             f"file because is a link.",
        single_directory_sentence=f"Skipping {len(settings_are_links)} "
                                  f"settings directory because is a link."
    )


def unlink_dotfiles(
    targets_list: dict[str, str],
    settings_dir: str,
    many_targets_sentence: str,
    single_file_sentence: str,
    single_directory_sentence: str,
    ask_for_confirmation: bool
) -> None:
    if targets_list:
        n_targets = len(targets_list.keys())

        print_dotfiles_to_manage(
            targets_list=targets_list,
            many_targets_sentence=many_targets_sentence,
            single_file_sentence=single_directory_sentence,
            single_directory_sentence=single_directory_sentence,
            symbol='-x->'
        )

        proceed = ask_to_proceed() if ask_for_confirmation else True

        if proceed:
            for i, (system_target_path, settings_target_path) in \
                    enumerate(targets_list.items(), 1):
                try:
                    print_action(
                        action_type='unlink',
                        system_target_path=system_target_path,
                        settings_target_path=settings_target_path
                    )
                    print(f"Total ({i}/{n_targets})", end='\r')

                    remove(path=system_target_path)
                    system_target_parent = os.path.dirname(system_target_path)
                    if not os.path.exists(system_target_parent):
                        os.makedirs(system_target_parent)
                    shutil.move(settings_target_path, system_target_path)
                    backup_path = generate_backup_path(path=system_target_path)
                    remove(path=backup_path)

                    parent_directory = os.path.dirname(settings_target_path)
                    protected_directories = (
                        settings_dir,
                        expand_home_path('~'),
                        '/'
                    )
                    while parent_directory not in protected_directories:
                        parent_directory_content = os.listdir(parent_directory)
                        if (not parent_directory_content or
                            ((len(parent_directory_content) == 1) and
                             parent_directory_content[0] == '.directory')):
                            shutil.rmtree(parent_directory)
                            parent_directory = \
                                os.path.dirname(parent_directory)
                        else:
                            break
                except Exception as e:
                    print_error(
                        f"Error in unlinking {system_target_path}. "
                        f"Check {LOG_FILE_PATH} for more details."
                    )
                    log_error(f"{e}")
        print('\n')


def _check_targets_to_be_unlinked(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and (
        (
            os.path.islink(system_target_path) and
            (os.readlink(system_target_path) == settings_target_path)
        ) or
        (
            not os.path.islink(system_target_path) and
            not os.path.exists(system_target_path)
        )
    )


def _check_wrong_existing_links(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and \
        os.path.islink(system_target_path) and \
        (os.readlink(system_target_path) != settings_target_path)


def _check_already_existing_system(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        os.path.exists(settings_target_path) and \
        not os.path.islink(system_target_path) and \
        os.path.exists(system_target_path)


def _check_already_unlinked_targets(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        not os.path.exists(settings_target_path) and \
        os.path.exists(system_target_path)


def _check_missing_settings_targets(
    system_target_path: str,
    settings_target_path: str
) -> bool:
    return not os.path.islink(settings_target_path) and \
        not os.path.exists(settings_target_path) and \
        not os.path.exists(system_target_path)


def _check_settings_are_links(settings_target_path: str) -> bool:
    return os.path.islink(settings_target_path)
