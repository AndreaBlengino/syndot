from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import lists, text, characters, dictionaries
from pytest import mark
from syndot.utils.commands import skip_dotfiles, print_dotfiles_to_manage
from tests.conftest import targets


@mark.utils
@mark.wip
class TestSkipDotfiles:

    @mark.genuine
    @given(
        targets_list=lists(elements=targets(), min_size=1, max_size=3),
        many_targets_sentence=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        single_file_sentence=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        single_directory_sentence=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_function(
        self,
        targets_list,
        many_targets_sentence,
        single_file_sentence,
        single_directory_sentence,
        capsys
    ):
        skip_dotfiles(
            targets_list=targets_list,
            many_targets_sentence=many_targets_sentence,
            single_file_sentence=single_file_sentence,
            single_directory_sentence=single_directory_sentence
        )
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output

        lines = printed_output.strip().split('\n')
        for line in lines[:-1]:
            assert line.startswith('Skip ')
            assert any([target in line for target in targets_list])
        if len(targets_list) > 1:
            assert many_targets_sentence in lines[-1]
        else:
            assert ((single_file_sentence in lines[-1]) or
                    (single_directory_sentence in lines[-1]))


@mark.utils
@mark.wip
class TestPrintDotfilesToManage:

    @mark.genuine
    @given(
        targets_list=dictionaries(
            keys=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            values=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            min_size=1,
            max_size=3
        ),
        many_targets_sentence=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        single_file_sentence=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        single_directory_sentence=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        symbol=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_function(
        self,
        targets_list,
        many_targets_sentence,
        single_file_sentence,
        single_directory_sentence,
        symbol,
        capsys
    ):
        print_dotfiles_to_manage(
            targets_list=targets_list,
            many_targets_sentence=many_targets_sentence,
            single_file_sentence=single_file_sentence,
            single_directory_sentence=single_directory_sentence,
            symbol=symbol
        )
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output
        for source, destination in targets_list.items():
            assert source in printed_output
            assert destination in printed_output
        assert symbol in printed_output
        if len(targets_list.keys()) == 1:
            assert (single_file_sentence in printed_output) or \
                   (single_directory_sentence in printed_output)
        else:
            assert many_targets_sentence in printed_output
