from syndot.utils.colors import Color


def print_action(
    action_type: str,
    system_target_path: str,
    settings_target_path: str
) -> None:
    if action_type == 'link':
        action = 'Linking'
        preposition = 'to'
        print(
            f"{action} {Color.link(system_target_path)} "
            f"{preposition} {Color.settings(settings_target_path)}"
        )
    elif action_type == 'unlink':
        action = 'Unlinking'
        preposition = 'from'
        print(
            f"{action} {Color.link(system_target_path)} {preposition} "
            f"{Color.settings(settings_target_path)}"
        )
    elif action_type == 'diffuse':
        action = 'Diffusing'
        preposition = 'to'
        print(
            f"{action} {Color.settings(settings_target_path)} {preposition} "
            f"{Color.link(system_target_path)}"
        )


def print_relationship(
    system_target_path: str,
    settings_target_path: str,
    symbol: str
) -> None:
    print(
        f"{Color.link(system_target_path)} {Color.symbol(symbol)} "
        f"{Color.settings(settings_target_path)}"
    )


def print_highlight(sentence: str, end: str = '\n') -> None:
    print(f"{Color.highlight(sentence)}", end=end)


def print_error(error: str, end: str = '\n') -> None:
    print(f"{Color.error(error)}", end=end)
