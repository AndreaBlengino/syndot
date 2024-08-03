import subprocess
from syndot.utils.colors import Color
from syndot.utils.system_info import gum_is_available


MESSAGE = 'Do you want to proceed?'
VALID_PROMPT_CHOICES = {
    'y': True,
    'ye': True,
    'yes': True,
    'n': False,
    'no': False
}
GUM_CONFIRM_COMMAND = [
    'gum',
    'confirm',
    f"{MESSAGE}",
    '--default=false',
    '--affirmative=YES',
    '--negative=NO',
    f"--prompt.foreground={Color.PROMPT_SENTENCE}",
    f"--selected.foreground={Color.PROMPT_BACKGROUND}",
    f"--selected.background={Color.PROMPT_FOREGROUND}",
    f"--unselected.foreground={Color.PROMPT_FOREGROUND}",
    f"--unselected.background={Color.PROMPT_BACKGROUND}"
]


def ask_to_proceed() -> bool:
    if gum_is_available():
        return __ask_to_proceed_gum()
    else:
        return __ask_to_proceed_prompt()


def __ask_to_proceed_prompt() -> bool:
    choice = ''
    while choice not in VALID_PROMPT_CHOICES:
        choice = input(f"{MESSAGE} (y/N)? ").lower()
        if choice == '':
            choice = 'n'

    return VALID_PROMPT_CHOICES[choice]


def __ask_to_proceed_gum() -> bool:
    choice = subprocess.run(
        '_'.join(GUM_CONFIRM_COMMAND).split('_'),
        stdout=subprocess.PIPE,
        text=True
    ).returncode

    return choice == 0
