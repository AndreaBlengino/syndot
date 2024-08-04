import os
import shutil
from syndot.utils.path import expand_home_path


def copy(source: str, destination: str) -> None:
    destination_parent = os.path.dirname(destination)
    if not os.path.exists(destination_parent):
        os.makedirs(destination_parent)

    if os.path.isfile(source):
        shutil.copy2(source, destination)
    elif os.path.isdir(source):
        shutil.copytree(source, destination, symlinks=True)
        st = os.stat(source)
        os.chown(destination, st.st_uid, st.st_gid)


def change_parent_owner(
    source: str,
    destination: str,
    settings_dir: str
) -> None:
    protected_directories = (
        expand_home_path(settings_dir),
        expand_home_path('~'),
        '/'
    )
    while destination not in protected_directories:
        st = os.stat(source)
        try:
            os.chown(destination, st.st_uid, st.st_gid)
        except PermissionError:
            pass
        source = os.path.dirname(source)
        destination = os.path.dirname(destination)


def change_child_owner(source: str, destination: str) -> None:
    source_content = os.listdir(source)
    destination_content = os.listdir(destination)
    for source_target, destination_target in \
            zip(source_content, destination_content):
        source_target_path = os.path.join(source, source_target)
        destination_target_path = os.path.join(destination, destination_target)
        st = os.stat(source_target_path)
        os.chown(destination_target_path, st.st_uid, st.st_gid)
        if os.path.isdir(destination_target_path):
            change_child_owner(
                source=source_target_path,
                destination=destination_target_path
            )


def remove(path: str) -> None:
    if os.path.islink(path):
        os.unlink(path)
    else:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
