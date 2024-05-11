from configparser import ConfigParser
import os


COLORSCHEME_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '_templates', 'default.colorscheme')
color_config = ConfigParser()
color_config.read(COLORSCHEME_TEMPLATE_PATH)
COLOR_MAP = {'link': 'Color6',
             'symbol': 'Color0',
             'settings': 'Color1'}


def get_ansi_color(color_type: str) -> str:
    color = color_config[COLOR_MAP[color_type]]['Color'].replace(',', ';')
    return f"\x1b[38;2;{color}m"


class Color:
    LINK_COLOR = get_ansi_color('link')
    SYMBOL_COLOR = get_ansi_color('symbol')
    SETTINGS_COLOR = get_ansi_color('settings')
    END_SEQUENCE = "\x1b[0m"

    @classmethod
    def link(cls, link: str) -> str:
        return cls.LINK_COLOR + link + cls.END_SEQUENCE

    @classmethod
    def symbol(cls, symbol: str) -> str:
        return cls.SYMBOL_COLOR + symbol + cls.END_SEQUENCE

    @classmethod
    def settings(cls, settings: str) -> str:
        return cls.SETTINGS_COLOR + settings + cls.END_SEQUENCE
