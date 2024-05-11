import os


def skip_dotfiles(targets_list: list[str],
                  many_targets_sentence: str,
                  single_file_sentence: str,
                  single_directory_sentence: str) -> None:
    if targets_list:
        if len(targets_list) > 1:
            print(many_targets_sentence)
        else:
            if os.path.isfile(targets_list[0]):
                print(single_file_sentence)
            else:
                print(single_directory_sentence)
        for target in targets_list:
            print(target)
        print()
