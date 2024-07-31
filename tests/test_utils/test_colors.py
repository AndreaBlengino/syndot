from hypothesis import given, settings
from hypothesis.strategies import text, characters
from pytest import mark
from syndot.utils.colors import Color


@mark.utils
class TestColor:

    @mark.genuine
    @given(
        link=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_link(self, link):
        colored_link = Color.link(link=link)

        assert isinstance(colored_link, str)
        assert colored_link
        assert link in colored_link
        assert colored_link.startswith(Color.LINK_COLOR)
        assert colored_link.endswith(Color.COLOR_END_SEQUENCE)

    @mark.genuine
    @given(
        symbol=text(
            min_size=1,
            max_size=3,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_symbol(self, symbol):
        colored_symbol = Color.symbol(symbol=symbol)

        assert isinstance(colored_symbol, str)
        assert colored_symbol
        assert symbol in colored_symbol
        assert colored_symbol.startswith(Color.SYMBOL_COLOR)
        assert colored_symbol.endswith(Color.COLOR_END_SEQUENCE)

    @mark.genuine
    @given(
        settings_=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_settings(self, settings_):
        colored_settings = Color.settings(settings=settings_)

        assert isinstance(colored_settings, str)
        assert colored_settings
        assert settings_ in colored_settings
        assert colored_settings.startswith(Color.SETTINGS_COLOR)
        assert colored_settings.endswith(Color.COLOR_END_SEQUENCE)

    @mark.genuine
    @given(
        error=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_error(self, error):
        colored_error = Color.error(error=error)

        assert isinstance(colored_error, str)
        assert colored_error
        assert error in colored_error
        assert colored_error.startswith(Color.ERROR_COLOR)
        assert colored_error.endswith(Color.COLOR_END_SEQUENCE)

    @mark.genuine
    @given(
        highlight=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_highlight(self, highlight):
        colored_highlight = Color.highlight(sentence=highlight)

        assert isinstance(colored_highlight, str)
        assert colored_highlight
        assert highlight in colored_highlight
        assert colored_highlight.startswith(Color.BOLD_START_SEQUENCE)
        assert colored_highlight.endswith(Color.BOLD_END_SEQUENCE)
