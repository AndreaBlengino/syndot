from hypothesis import given, settings
from hypothesis.strategies import lists, text, characters
from pytest import mark
from syndot.utils.gum_style import complete_gum_filter_command


@mark.utils
class TestGumStyle:

    @mark.genuine
    @given(
        labels=lists(
            elements=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            min_size=3,
            max_size=5
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_link(self, labels):
        gum_filter_command = complete_gum_filter_command(labels=labels)

        assert isinstance(gum_filter_command, list)
        assert gum_filter_command
        assert all(
            [isinstance(command, str) for command in gum_filter_command]
        )
        options = [
            'gum',
            'filter',
            '--prompt= ',
            '--placeholder=Filter labels',
            '--width=100',
            '--no-limit'
        ]
        assert all([option in gum_filter_command for option in options])
