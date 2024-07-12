from hypothesis import given, settings
from hypothesis.strategies import sampled_from
from pytest import mark
from syndot.utils.prompt import VALID_PROMPT_CHOICES
from syndot.utils import prompt


ok_to_proceed = []
not_ok_to_proceed = []
for input_answer, proceed in VALID_PROMPT_CHOICES.items():
    if proceed:
        ok_to_proceed.append(input_answer)
    else:
        not_ok_to_proceed.append(input_answer)


@mark.utils
class TestAskToProceed:

    @mark.genuine
    @given(answer=sampled_from(elements=[*VALID_PROMPT_CHOICES.keys(), '']))
    @settings(max_examples=100, deadline=None)
    def test_function(self, answer):
        prompt.input = lambda x: answer
        proceed = prompt.ask_to_proceed()

        if answer in ok_to_proceed:
            assert proceed
        elif answer in not_ok_to_proceed:
            assert not proceed

    @staticmethod
    def teardown_method():
        prompt.input = input
