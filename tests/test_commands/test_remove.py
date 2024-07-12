from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings
from hypothesis.strategies import booleans
import os
from pytest import mark, raises
from syndot.commands import remove
from tests.conftest import labels, targets, reset_environment
from tests.test_commands.conftest import (
    generate_add_and_remove_testing_system_files, generate_testing_map_file,
    TEST_MAP_FILE_PATH)


@mark.commands
class TestRemove:

    @mark.genuine
    @given(target_label=labels(),
           target_path=targets(absolute=False),
           ending_separator=booleans(),
           target_is_label=booleans())
    @settings(max_examples=100, deadline=None)
    def test_function(
            self, target_label, target_path, ending_separator,
            target_is_label):
        reset_environment()

        args = Namespace()
        if target_is_label:
            args.label = [target_label]
            args.path = None
        else:
            args.label = None
            if ending_separator:
                args.path = [target_path + os.sep]
            else:
                args.path = [target_path]
        args.mapfile = TEST_MAP_FILE_PATH

        generate_testing_map_file()
        generate_add_and_remove_testing_system_files()

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        assert target_label in config['Targets'].keys()
        assert target_path in path_list

        remove(args=args)

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        if target_is_label:
            assert target_label not in config['Targets'].keys()
        assert target_path not in path_list

        reset_environment()

    @mark.error
    @given(target_label=labels(),
           target_path=targets(absolute=False),
           ending_separator=booleans())
    @settings(max_examples=100, deadline=None)
    def test_raises_name_error(
            self, target_label, target_path, ending_separator):
        reset_environment()

        args = Namespace()
        args.label = target_label
        if ending_separator:
            args.path = [target_path + '_other' + os.sep]
        else:
            args.path = [target_path + '_other']
        args.mapfile = TEST_MAP_FILE_PATH

        generate_testing_map_file()
        generate_add_and_remove_testing_system_files()

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        assert target_label in config['Targets'].keys()
        assert target_path in path_list

        with raises(NameError):
            remove(args=args)

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())

        assert target_label in config['Targets'].keys()
        assert target_path in path_list

        reset_environment()
