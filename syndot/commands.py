import os
import shutil
from syndot import utils


def link(source_target_path: str, destination_target_path: str, backup: bool) -> None:
    if backup:
        utils.copy(source = source_target_path, destination = destination_target_path)
        backup_path = utils.generate_backup_path(path = source_target_path)
        os.rename(source_target_path, backup_path)
    else:
        shutil.move(source_target_path, destination_target_path)
    os.symlink(destination_target_path, source_target_path)


def unlink(source_target_path: str, destination_target_path: str) -> None:
    utils.remove(path = source_target_path)
    shutil.move(destination_target_path, source_target_path)
    backup_path = utils.generate_backup_path(path = source_target_path)
    utils.remove(path = backup_path)


def diffuse(source_target_path: str, destination_target_path: str) -> None:
    os.symlink(destination_target_path, source_target_path)
