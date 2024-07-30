from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings
from hypothesis.strategies import booleans, sampled_from
import os
from pytest import mark, raises
from syndot.commands.add import add
from tests.conftest import labels, targets, reset_environment
from tests.test_commands.conftest import (
    generate_add_and_remove_testing_system_files, generate_testing_map_file,
    empty_testing_map_file, TEST_MAP_FILE_PATH)


@mark.commands
class TestAdd:

    @mark.genuine
    @given(target_label=labels(),
           target_path=targets(absolute=False),
           target_status=sampled_from(elements=['targets_to_be_added',
                                                'already_added_target']),
           ending_separator=booleans())
    @settings(max_examples=100, deadline=None)
    def test_function(
            self, target_label, target_path, target_status, ending_separator):
        reset_environment()

        args = Namespace()
        args.label = target_label
        if ending_separator:
            args.path = [target_path + os.sep]
        else:
            args.path = [target_path]
        args.mapfile = TEST_MAP_FILE_PATH

        generate_testing_map_file()
        generate_add_and_remove_testing_system_files()

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)
        if target_status == 'targets_to_be_added':
            empty_testing_map_file()

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        if target_status == 'targets_to_be_added':
            assert target_label not in config['Targets'].keys()
            assert target_path not in path_list
        if target_status == 'already_added_target':
            assert target_label in config['Targets'].keys()
            assert target_path in path_list

        add(args=args)

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)

        assert target_label in config['Targets'].keys()
        assert target_path in config['Targets'][target_label].split()

        reset_environment()

    @mark.error
    @given(target_label=labels(),
           target_path=targets(absolute=False),
           ending_separator=booleans())
    @settings(max_examples=100, deadline=None)
    def test_raises_OS_error(
            self, target_label, target_path, ending_separator):
        reset_environment()

        args = Namespace()
        args.label = target_label
        if ending_separator:
            args.path = [target_path + os.sep]
        else:
            args.path = [target_path]
        args.mapfile = TEST_MAP_FILE_PATH

        generate_testing_map_file()

        assert not os.path.exists(target_path)
        empty_testing_map_file()

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        assert target_label not in config['Targets'].keys()
        assert target_path not in path_list

        with raises(OSError):
            add(args=args)

        assert not os.path.exists(target_path)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        assert target_label not in config['Targets'].keys()
        assert target_path not in path_list

        reset_environment()
