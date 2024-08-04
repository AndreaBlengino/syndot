from configparser import ConfigParser
import os
from syndot.init_config import CONFIG_DIR_PATH


COLORSCHEME_PATH = os.path.join(
    CONFIG_DIR_PATH,
    'colorschemes',
    'default.colorscheme'
)
if not os.path.exists(CONFIG_DIR_PATH) or not os.path.exists(COLORSCHEME_PATH):
    COLORSCHEME_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '_colorschemes',
        'default.colorscheme'
    )
color_config = ConfigParser()
color_config.read(COLORSCHEME_PATH)
COLOR_MAP = {
    'link': 'color13',
    'symbol': 'color11',
    'settings': 'color08',
    'error': 'color05',
    'prompt_sentence': 'color07',
    'prompt_foreground': 'color07',
    'prompt_background': 'color24',
    'indicator_foreground': 'color12',
    'match_foreground': 'color07',
    'selected_indicator_foreground': 'color09'
}


def _get_color(category: str, fmt: str) -> str:
    hex_color = color_config.get(section='Colors', option=COLOR_MAP[category])
    if fmt == 'HEX':
        return hex_color
    elif fmt == 'RGB':
        r, g, b = tuple(
            int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)
        )
        return f"{r};{g};{b}"
    else:
        raise ValueError("Invalid color format: select 'HEX' or 'RGB'.")


def _rgb_to_ansi(rgb_color: str) -> str:
    return f"\x1b[38;2;{rgb_color}m"


class Color:
    LINK_COLOR = _rgb_to_ansi(_get_color(category='link', fmt='RGB'))
    SYMBOL_COLOR = _rgb_to_ansi(_get_color(category='symbol', fmt='RGB'))
    SETTINGS_COLOR = _rgb_to_ansi(_get_color(category='settings', fmt='RGB'))
    ERROR_COLOR = _rgb_to_ansi(_get_color(category='error', fmt='RGB'))
    PROMPT_SENTENCE = _get_color(category='prompt_sentence', fmt='HEX')
    PROMPT_FOREGROUND = _get_color(category='prompt_foreground', fmt='HEX')
    PROMPT_BACKGROUND = _get_color(category='prompt_background', fmt='HEX')
    INDICATOR_FOREGROUND = _get_color(
        category='indicator_foreground',
        fmt='HEX'
    )
    MATCH_FOREGROUND = _get_color(category='match_foreground', fmt='HEX')
    SELECTED_INDICATOR_FOREGROUND = _get_color(
        category='selected_indicator_foreground',
        fmt='HEX'
    )
    BOLD_START_SEQUENCE = '\033[1m'
    BOLD_END_SEQUENCE = '\033[0m'
    COLOR_END_SEQUENCE = '\x1b[0m'

    @classmethod
    def link(cls, link: str) -> str:
        return cls.LINK_COLOR + link + cls.COLOR_END_SEQUENCE

    @classmethod
    def symbol(cls, symbol: str) -> str:
        return cls.SYMBOL_COLOR + symbol + cls.COLOR_END_SEQUENCE

    @classmethod
    def settings(cls, settings: str) -> str:
        return cls.SETTINGS_COLOR + settings + cls.COLOR_END_SEQUENCE

    @classmethod
    def error(cls, error: str) -> str:
        return cls.ERROR_COLOR + error + cls.COLOR_END_SEQUENCE

    @classmethod
    def highlight(cls, sentence: str) -> str:
        return cls.BOLD_START_SEQUENCE + sentence + cls.BOLD_END_SEQUENCE
