from argparse import Namespace
from hypothesis import given, settings
from hypothesis.strategies import one_of, none, booleans, sampled_from
import os
from pytest import mark
import shutil
from syndot.commands import link
from syndot.utils import prompt
from syndot.utils.prompt import VALID_PROMPT_CHOICES
from tests.conftest import targets, valid_targets, TEST_DATA_PATH, SETTINGS_DIR
from tests.test_commands.conftest import generate_testing_system_files, generate_testing_map_file, TEST_MAP_FILE_PATH


@mark.utils
class TestLink:

    @mark.genuine
    @given(exact_match = booleans(),
           target_path = one_of(targets(absolute = False), none()),
           truncate_path = booleans(),
           backup = booleans(),
           answer = sampled_from(elements = [*VALID_PROMPT_CHOICES.keys(), '']),
           target_status = sampled_from(elements = ['targets_to_be_linked', 'already_existing_settings',
                                                    'missing_system_targets', 'already_linked_targets',
                                                    'corrupted_targets', 'wrong_existing_links']))
    @settings(max_examples = 100, deadline = None)
    def test_function(self, exact_match, target_path, truncate_path, backup, answer, target_status):

        args = Namespace()
        args.mapfile = TEST_MAP_FILE_PATH
        args.all = target_path is None
        args.exact = exact_match
        truncated_target_path = os.path.split(target_path)[0] if truncate_path and target_path is not None else target_path
        args.TARGET_PATH_START = truncated_target_path
        args.backup = backup

        generate_testing_map_file()
        generate_testing_system_files(status = target_status)

        target_list = [target.replace('~', os.path.join(os.getcwd(), TEST_DATA_PATH)) for target in valid_targets]
        if target_path:
            if exact_match:
                target_list = [target for target in target_list if target == truncated_target_path]
            else:
                target_list = [target for target in target_list if target.startswith(truncated_target_path)]
        if target_status == 'targets_to_be_linked':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.exists(target)
                assert not os.path.islink(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'already_existing_settings':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.exists(target)
                assert not os.path.islink(target)
                assert os.path.exists(settings_target_path)
        elif target_status == 'missing_system_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'already_linked_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'corrupted_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert not os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) != settings_target_path

        prompt.input = lambda x: answer
        link(args = args)

        if target_status == 'targets_to_be_linked':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer]:
                    assert os.path.islink(target)
                    assert os.readlink(target) == settings_target_path
                    assert os.path.exists(settings_target_path)
                    if backup:
                        if os.path.isfile(settings_target_path):
                            backup_path = target + '.bak'
                            assert os.path.exists(backup_path)
                            assert os.path.isfile(backup_path)
                        elif os.path.isdir(settings_target_path):
                            backup_path = target + '_bak'
                            assert os.path.isdir(backup_path)
                else:
                    assert os.path.exists(target)
                    assert not os.path.islink(target)
                    assert not os.path.exists(settings_target_path)
        elif target_status == 'already_existing_settings':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer]:
                    assert os.path.islink(target)
                    assert os.readlink(target) == settings_target_path
                    assert os.path.exists(settings_target_path)
                    if backup:
                        if os.path.isfile(settings_target_path):
                            backup_path = target + '.bak'
                            assert os.path.exists(backup_path)
                            assert os.path.isfile(backup_path)
                        elif os.path.isdir(settings_target_path):
                            backup_path = target + '_bak'
                            assert os.path.isdir(backup_path)
                else:
                    assert os.path.exists(target)
                    assert not os.path.islink(target)
                    assert os.path.exists(settings_target_path)
        elif target_status == 'missing_system_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'already_linked_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'corrupted_targets':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert not os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = os.path.join(os.getcwd(), SETTINGS_DIR, *target.split(os.path.sep)[1:])
                assert os.path.islink(target)
                assert os.readlink(target) != settings_target_path

        shutil.rmtree(TEST_DATA_PATH)

    @staticmethod
    def teardown_method():
        prompt.input = input
