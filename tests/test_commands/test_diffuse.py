from argparse import Namespace
from hypothesis import given, settings
from hypothesis.strategies import one_of, none, sampled_from, booleans
import os
from pytest import mark
from syndot.commands import diffuse
from syndot.utils import prompt
from syndot.utils.prompt import VALID_PROMPT_CHOICES
from tests.conftest import (labels, targets, valid_targets, TEST_DATA_PATH,
                            reset_environment)
from tests.test_commands.conftest import (
    generate_diffuse_testing_system_files, generate_testing_map_file,
    TEST_MAP_FILE_PATH, get_settings_target_path)


@mark.commands
class TestDiffuse:

    @mark.genuine
    @given(target_label=one_of(labels(), none()),
           target_path=one_of(targets(absolute=False), none()),
           start_path=booleans(),
           answer=sampled_from(elements=[*VALID_PROMPT_CHOICES.keys(), '']),
           target_status=sampled_from(
               elements=['targets_to_be_diffused', 'already_existing_system',
                         'already_diffused_targets', 'wrong_existing_links',
                         'missing_settings_targets', 'settings_are_links']))
    @settings(max_examples=100, deadline=None)
    def test_function(
            self, target_label, target_path, start_path, answer,
            target_status):
        reset_environment()

        args = Namespace()
        if target_label:
            args.label = [target_label]
        else:
            args.label = None
        args.mapfile = TEST_MAP_FILE_PATH
        if target_path:
            args.path = [target_path]
        else:
            args.path = None
        args.start = os.path.split(target_path)[0] \
            if start_path and target_path else None

        generate_testing_map_file()
        generate_diffuse_testing_system_files(status=target_status)

        target_list = [target.replace(
                       '~', os.path.join(os.getcwd(), TEST_DATA_PATH))
                       for target in valid_targets]
        if target_path:
            target_list = [target for target in target_list
                           if target == target_path]
        if target_status == 'targets_to_be_diffused':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert not os.path.exists(target)
                assert not os.path.islink(target)
                assert os.path.exists(settings_target_path)
        elif target_status == 'already_existing_system':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.exists(target)
                assert not os.path.islink(target)
                assert os.path.exists(settings_target_path)
        elif target_status == 'already_diffused_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) != settings_target_path
        elif target_status == 'missing_settings_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'settings_are_links':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(settings_target_path)

        prompt.input = lambda x: answer
        diffuse.diffuse(args=args)

        if target_status == 'targets_to_be_diffused':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer]:
                    assert os.path.islink(target)
                    assert os.readlink(target) == settings_target_path
                    assert os.path.exists(settings_target_path)
                else:
                    assert not os.path.exists(target)
                    assert not os.path.islink(target)
                    assert os.path.exists(settings_target_path)
        elif target_status == 'already_existing_system':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer]:
                    assert os.path.islink(target)
                    assert os.readlink(target) == settings_target_path
                    assert os.path.exists(settings_target_path)
                else:
                    assert os.path.exists(target)
                    assert not os.path.islink(target)
                    assert os.path.exists(settings_target_path)
        elif target_status == 'already_diffused_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer]:
                    assert os.path.islink(target)
                    assert os.readlink(target) == settings_target_path
                    assert os.path.exists(settings_target_path)
                else:
                    assert os.path.islink(target)
                    assert os.readlink(target) != settings_target_path
        elif target_status == 'missing_settings_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'settings_are_links':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(settings_target_path)

        reset_environment()

    @staticmethod
    def teardown_method():
        prompt.input = input
