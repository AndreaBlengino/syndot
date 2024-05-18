from configparser import ConfigParser
import os
from syndot.init_config import CONFIG_DIR_PATH


COLORSCHEME_PATH = os.path.join(CONFIG_DIR_PATH, 'colorschemes', 'default.colorscheme')
if not os.path.exists(CONFIG_DIR_PATH) or not os.path.exists(COLORSCHEME_PATH):
    COLORSCHEME_PATH = os.path.join(os.path.dirname(__file__), '_colorschemes', 'default.colorscheme')
color_config = ConfigParser()
color_config.read(COLORSCHEME_PATH)
COLOR_MAP = {'link': 'Color6',
             'symbol': 'Color0',
             'settings': 'Color1',
             'error': 'Color4'}


def get_ansi_color(color_type: str) -> str:
    color = color_config.get(section = COLOR_MAP[color_type], option = 'Color').replace(',', ';')
    return f"\x1b[38;2;{color}m"


class Color:
    LINK_COLOR = get_ansi_color('link')
    SYMBOL_COLOR = get_ansi_color('symbol')
    SETTINGS_COLOR = get_ansi_color('settings')
    ERROR_COLOR = get_ansi_color('error')
    BOLD_START_SEQUENCE = "\033[1m"
    BOLD_END_SEQUENCE = "\033[0m"
    COLOR_END_SEQUENCE = "\x1b[0m"

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
