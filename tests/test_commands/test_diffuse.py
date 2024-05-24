from argparse import Namespace
from hypothesis import given, settings
from hypothesis.strategies import one_of, none, booleans, sampled_from
import os
from pytest import mark
import shutil
from syndot.commands import diffuse
from syndot.utils import prompt
from syndot.utils.prompt import VALID_PROMPT_CHOICES
from tests.conftest import targets, valid_targets, TEST_DATA_PATH, SETTINGS_DIR
from tests.test_commands.conftest import generate_diffuse_testing_system_files, generate_testing_map_file, TEST_MAP_FILE_PATH


@mark.commands
class TestDiffuse:

    @mark.genuine
    @given(exact_match = booleans(),
           target_path = one_of(targets(absolute = False), none()),
           truncate_path = booleans(),
           answer = sampled_from(elements = [*VALID_PROMPT_CHOICES.keys(), '']),
           target_status = sampled_from(elements = ['targets_to_be_diffused', 'already_existing_system',
                                                    'already_diffused_targets', 'wrong_existing_links',
                                                    'missing_settings_targets', 'settings_are_links']))
    @settings(max_examples = 100, deadline = None)
    def test_function(self, exact_match, target_path, truncate_path, answer, target_status):

        args = Namespace()
        args.mapfile = TEST_MAP_FILE_PATH
        args.all = target_path is None
        args.exact = exact_match
        truncated_target_path = os.path.split(target_path)[0] if truncate_path and target_path is not None else target_path
        args.TARGET_PATH_START = truncated_target_path

        generate_testing_map_file()
        generate_diffuse_testing_system_files(status = target_status)

        target_list = [target.replace('~', os.path.join(os.getcwd(), TEST_DATA_PATH)) for target in valid_targets]
        if target_path:
            if exact_match:
                target_list = [target for target in target_list if target == truncated_target_path]
            else:
                target_list = [target for target in target_list if target.startswith(truncated_target_path)]
        if target_status == 'targets_to_be_diffused':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert not os.path.exists(target)
                assert not os.path.islink(target)
                assert os.path.exists(settings_target_path)
        elif target_status == 'already_existing_system':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.exists(target)
                assert not os.path.islink(target)
                assert os.path.exists(settings_target_path)
        elif target_status == 'already_diffused_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) != settings_target_path
        elif target_status == 'missing_settings_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'settings_are_links':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(settings_target_path)

        prompt.input = lambda x: answer
        diffuse(args = args)

        if target_status == 'targets_to_be_diffused':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
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
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
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
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
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
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'settings_are_links':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(settings_target_path)

        shutil.rmtree(TEST_DATA_PATH)

    @staticmethod
    def teardown_method():
        prompt.input = input
