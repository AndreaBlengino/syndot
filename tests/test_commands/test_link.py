from argparse import Namespace
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import one_of, none, booleans, sampled_from
import os
from pytest import mark
from syndot.commands import link
from syndot.utils import prompt
from syndot.utils.prompt import VALID_PROMPT_CHOICES
from tests.conftest import (
    labels,
    targets,
    valid_targets,
    TEST_DATA_PATH,
    reset_environment
)
from tests.test_commands.conftest import (
    generate_link_testing_system_files,
    generate_testing_map_file,
    TEST_MAP_FILE_PATH,
    get_settings_target_path
)


@mark.commands
class TestLink:

    @mark.genuine
    @given(
        backup=booleans(),
        target_label=one_of(labels(), none()),
        target_path=one_of(targets(absolute=False), none()),
        start_path=booleans(),
        no_confirm=booleans(),
        answer=sampled_from(elements=[*VALID_PROMPT_CHOICES.keys(), '']),
        target_status=sampled_from(
            elements=[
                'targets_to_be_linked',
                'already_existing_settings',
                'missing_system_targets',
                'already_linked_targets',
                'corrupted_targets',
                'wrong_existing_links'
            ]
        )
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_function(
        self,
        target_label,
        target_path,
        start_path,
        no_confirm,
        backup,
        answer,
        target_status,
        monkeypatch
    ):
        reset_environment()

        args = Namespace()
        args.backup = backup
        if target_label:
            if target_path:
                args.label = None
                args.path = None
            else:
                args.label = [target_label]
                args.path = None
        else:
            if target_path:
                args.label = None
                args.path = [target_path]
            else:
                args.label = None
                args.path = None
        args.mapfile = TEST_MAP_FILE_PATH
        args.start = os.path.split(target_path)[0] \
            if start_path and target_path else None
        args.no_confirm = no_confirm
        args.interactive = False

        generate_testing_map_file()
        generate_link_testing_system_files(status=target_status)

        target_list = [
            target.replace(
                '~',
                os.path.join(os.getcwd(), TEST_DATA_PATH)
            ) for target in valid_targets
        ]
        if target_path:
            target_list = [target for target in target_list
                           if target == target_path]
        if target_status == 'targets_to_be_linked':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.exists(target)
                assert not os.path.islink(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'already_existing_settings':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.exists(target)
                assert not os.path.islink(target)
                assert os.path.exists(settings_target_path)
        elif target_status == 'missing_system_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'already_linked_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'corrupted_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert not os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) != settings_target_path

        monkeypatch.setattr(
            link,
            'ask_to_proceed',
            lambda: VALID_PROMPT_CHOICES[answer] if answer else False
        )

        prompt.input = lambda x: answer
        link.link(args=args)

        if target_status == 'targets_to_be_linked':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer] or no_confirm:
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
                settings_target_path = get_settings_target_path(target=target)
                if answer == '':
                    answer = 'n'
                if VALID_PROMPT_CHOICES[answer] or no_confirm:
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
                settings_target_path = get_settings_target_path(target=target)
                assert not os.path.exists(target)
                assert not os.path.exists(settings_target_path)
        elif target_status == 'already_linked_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert os.path.exists(settings_target_path)
        elif target_status == 'corrupted_targets':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) == settings_target_path
                assert not os.path.exists(settings_target_path)
        elif target_status == 'wrong_existing_links':
            for target in target_list:
                settings_target_path = get_settings_target_path(target=target)
                assert os.path.islink(target)
                assert os.readlink(target) != settings_target_path

        reset_environment()

    @staticmethod
    def teardown_method():
        prompt.input = input
