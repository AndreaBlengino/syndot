from configparser import ConfigParser
import os
from syndot.init_config import CONFIG_DIR_PATH
from syndot.utils.colors import Color


STYLE_PATH = os.path.join(
    CONFIG_DIR_PATH,
    '_templates',
    'style.ini'
)
if not os.path.exists(CONFIG_DIR_PATH) or not os.path.exists(STYLE_PATH):
    STYLE_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '_templates',
        'style.ini'
    )

style_config = ConfigParser()
style_config.read(STYLE_PATH)

indicator = style_config['gum']['indicator'].replace('\'', '')
indicator_foreground = Color.INDICATOR_FOREGROUND
selected_prefix = style_config['gum']['selected_prefix'].replace('\'', '')
selected_indicator_foreground = Color.SELECTED_INDICATOR_FOREGROUND
unselected_prefix = style_config['gum']['unselected_prefix'].replace('\'', '')
match_foreground = Color.MATCH_FOREGROUND

GUM_FILTER_COMMAND = [
    'gum',
    'filter'
]
GUM_OPTIONS = [
    '--prompt= ',
    '--placeholder=Filter labels',
    '--width=100',
    '--no-limit',
    f"--indicator={indicator}",
    f"--indicator.foreground={indicator_foreground}",
    f"--selected-prefix={selected_prefix}",
    f"--selected-indicator.foreground={selected_indicator_foreground}",
    f"--unselected-prefix={unselected_prefix}",
    f"--match.foreground={match_foreground}"
]

if style_config['gum']['match_bold'] in ['True', 'true']:
    GUM_OPTIONS.append('--match.bold')


def complete_gum_filter_command(labels: list[str]) -> list[str]:
    GUM_FILTER_COMMAND.extend(labels)
    GUM_FILTER_COMMAND.extend(GUM_OPTIONS)

    return GUM_FILTER_COMMAND
