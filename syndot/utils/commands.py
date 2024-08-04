import os
from syndot.utils.print_ import print_highlight, print_relationship


def skip_dotfiles(
    targets_list: list[str],
    many_targets_sentence: str,
    single_file_sentence: str,
    single_directory_sentence: str
) -> None:
    if targets_list:
        for target in targets_list:
            print(f"Skip {target}")
        if len(targets_list) > 1:
            print_highlight(many_targets_sentence)
        else:
            if os.path.isfile(targets_list[0]):
                print_highlight(single_file_sentence)
            else:
                print_highlight(single_directory_sentence)
        print()


def print_dotfiles_to_manage(
    targets_list: dict[str, str],
    many_targets_sentence: str,
    single_file_sentence: str,
    single_directory_sentence: str,
    symbol: str
) -> None:
    n_targets = len(targets_list.keys())
    if n_targets > 1:
        for system_target_path, settings_target_path in targets_list.items():
            print_relationship(
                system_target_path=system_target_path,
                settings_target_path=settings_target_path,
                symbol=symbol
            )
        print_highlight(many_targets_sentence)
    else:
        print_relationship(
            system_target_path=list(targets_list.keys())[0],
            settings_target_path=list(targets_list.values())[0],
            symbol=symbol
        )
        if os.path.isfile(list(targets_list.keys())[0]):
            print_highlight(single_file_sentence)
        else:
            print_highlight(single_directory_sentence)
