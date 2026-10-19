import re
import subprocess


def _get_version() -> str:
    try:
        tag = subprocess.check_output(
            [
                "git",
                "describe",
                "--tags",
                "--abbrev=0",
                "--match",
                "[0-9]*.[0-9]*.[0-9]*",
            ],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        tag = "0.0.0"

    return tag if re.fullmatch(r"\d+\.\d+\.\d+", tag) else "0.0.0"


__version__ = _get_version()
