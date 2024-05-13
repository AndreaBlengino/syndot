import os
from syndot.utils.print_ import print_highlight


def skip_dotfiles(targets_list: list[str],
                  many_targets_sentence: str,
                  single_file_sentence: str,
                  single_directory_sentence: str) -> None:
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
