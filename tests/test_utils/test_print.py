from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import sampled_from, text, characters
from pytest import mark
from syndot.utils.print_ import print_action, print_relationship, print_highlight, print_error
from tests.conftest import paths


@mark.utils
class TestPrint:

    @mark.genuine
    @given(action = sampled_from(elements = ['link', 'unlink', 'diffuse']),
           system_target_path = paths(),
           settings_target_path = paths())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.function_scoped_fixture])
    def test_print_action(self, action, system_target_path, settings_target_path, capsys):
        print_action(action_type = action,
                     system_target_path = system_target_path,
                     settings_target_path = settings_target_path)
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output
        assert system_target_path in printed_output
        assert settings_target_path in printed_output
        if action == 'link':
            assert printed_output.startswith('Linking')
            assert 'to' in printed_output
        elif action == 'unlink':
            assert printed_output.startswith('Unlink')
            assert 'from' in printed_output
        elif action == 'diffuse':
            assert printed_output.startswith('Diffusing')
            assert 'to' in printed_output

    @mark.genuine
    @given(symbol = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)),
           system_target_path = paths(),
           settings_target_path = paths())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.function_scoped_fixture])
    def test_relationship(self, symbol, system_target_path, settings_target_path, capsys):
        print_relationship(system_target_path = system_target_path,
                           settings_target_path = settings_target_path,
                           symbol = symbol)
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output
        assert system_target_path in printed_output
        assert settings_target_path in printed_output
        assert symbol in printed_output

    @mark.genuine
    @given(sentence = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)))
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.function_scoped_fixture])
    def test_highlight(self, sentence, capsys):
        print_highlight(sentence = sentence)
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output
        assert sentence in printed_output

    @mark.genuine
    @given(error = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)))
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.function_scoped_fixture])
    def test_error(self, error, capsys):
        print_error(error = error)
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output
        assert error in printed_output
