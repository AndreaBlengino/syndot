import subprocess


def gum_is_available() -> bool:
    return not subprocess.run(
        'which gum'.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    ).returncode
