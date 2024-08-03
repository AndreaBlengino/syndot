from argparse import Namespace
from configparser import ConfigParser
import os
import subprocess
from syndot.utils.path import expand_home_path
from syndot.utils.system_info import gum_is_available
from syndot.utils.gum_style import complete_gum_filter_command


def read_map_file(map_file_path: str | None) -> ConfigParser:
    map_file_path = expand_home_path(
        map_file_path if map_file_path is not None else 'map.ini'
    )
    if not os.path.exists(map_file_path):
        if map_file_path == 'map.ini':
            raise FileNotFoundError(
                "Missing map.ini file in current directory."
            )
        else:
            raise FileNotFoundError(
                "Missing map.ini file at the specified path."
            )
    config = ConfigParser()
    config.read(map_file_path)

    return config


def get_map_info(
    config: ConfigParser,
    args: Namespace
) -> tuple[str, list[str]]:
    settings_dir = config['Path']['settings_dir']
    targets, unavailable_labels, unavailable_paths = _get_available_targets(
        config=config,
        args=args
    )

    _compose_error_message(
        unavailable_labels=unavailable_labels,
        unavailable_paths=unavailable_paths
    )

    if args.interactive:
        if gum_is_available():
            gum_filter_command = complete_gum_filter_command(
                labels=list(config['Targets'].keys())
            )
            selected_labels = subprocess.run(
                gum_filter_command,
                stdout=subprocess.PIPE
            ).stdout.decode('utf-8').split()
            targets = [path for selected_label in selected_labels
                       for path in config['Targets'][selected_label].split()]
        else:
            raise OSError("Interactive option requires 'gum', which is not "
                          "available in the system")
    else:
        if args.label is None and args.path is None:
            for target in config['Targets'].values():
                targets.extend(target.split())

    if args.start:
        targets = [target for target in targets
                   if target.startswith(args.start)]

    return settings_dir, targets


def write_map_file(map_file_path: str | None, config: ConfigParser) -> None:
    with open(map_file_path, 'w') as map_file:
        config.write(map_file)


def _get_available_targets(
    config: ConfigParser,
    args: Namespace
) -> tuple[list[str], [list[str], list[str]]]:
    targets = []

    available_labels = list(config['Targets'].keys())
    unavailable_labels = []
    if args.label is not None:
        for label in args.label:
            if label in available_labels:
                targets.extend(config['Targets'][label].split())
            else:
                unavailable_labels.append(label)

    available_paths = []
    for path in config['Targets'].values():
        available_paths.extend(path.split())
    available_paths = [expand_home_path(path) for path in available_paths]
    unavailable_paths = []
    if args.path is not None:
        for path in args.path:
            if path.endswith(os.sep):
                path = path[:-1]
            path = expand_home_path(path=path)
            if path in available_paths:
                targets.append(path)
            else:
                unavailable_paths.append(path)

    return targets, unavailable_labels, unavailable_paths


def _compose_error_message(
    unavailable_labels: list[str],
    unavailable_paths: list[str]
) -> None:
    error_message = ""
    if unavailable_labels:
        error_message += "\nThe following labels are not available in the map"\
                         "file:\n"
        for label in unavailable_labels:
            error_message += f"    {label}\n"
    if unavailable_paths:
        error_message += "\nThe following paths are not available in the map"\
                         "file:\n"
        for path in unavailable_paths:
            error_message += f"    {path}\n"
    if error_message:
        raise NameError(error_message)
