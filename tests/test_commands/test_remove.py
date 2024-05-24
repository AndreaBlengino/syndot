from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings
from hypothesis.strategies import booleans
import os
from pytest import mark, raises
import shutil
from syndot.commands import remove
from tests.conftest import targets, TEST_DATA_PATH
from tests.test_commands.conftest import (generate_add_and_remove_testing_system_files, generate_testing_map_file,
                                          TEST_MAP_FILE_PATH)


@mark.commands
class TestRemove:

    @mark.genuine
    @given(target_path = targets(absolute = False), ending_separator = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, target_path, ending_separator):

        args = Namespace()
        args.mapfile = TEST_MAP_FILE_PATH
        if ending_separator:
            args.TARGET_PATH = target_path + os.sep
        else:
            args.TARGET_PATH = target_path

        generate_testing_map_file()
        generate_add_and_remove_testing_system_files()

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)
        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        if os.path.isfile(target_path):
            assert target_path in config['Targets']['files']
        if os.path.isdir(target_path):
            assert target_path in config['Targets']['directories']

        remove(args = args)

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)
        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        if os.path.isfile(target_path):
            assert target_path not in config['Targets']['files'].split()
        if os.path.isdir(target_path):
            assert target_path not in config['Targets']['directories'].split()

        shutil.rmtree(TEST_DATA_PATH)

    @mark.error
    @given(target_path = targets(absolute = False),
           ending_separator = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_raises_name_error(self, target_path, ending_separator):

        args = Namespace()
        args.mapfile = TEST_MAP_FILE_PATH
        if ending_separator:
            args.TARGET_PATH = target_path + '_other' + os.sep
        else:
            args.TARGET_PATH = target_path + '_other'

        generate_testing_map_file()
        generate_add_and_remove_testing_system_files()

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)
        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        if os.path.isfile(target_path):
            assert target_path in config['Targets']['files']
        if os.path.isdir(target_path):
            assert target_path in config['Targets']['directories']

        with raises(NameError):
            remove(args = args)

        assert os.path.exists(target_path)
        assert not os.path.islink(target_path)
        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        if os.path.isfile(target_path):
            assert target_path in config['Targets']['files'].split()
        if os.path.isdir(target_path):
            assert target_path in config['Targets']['directories'].split()

        shutil.rmtree(TEST_DATA_PATH)
