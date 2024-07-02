from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings
from hypothesis.strategies import booleans, one_of, none, lists
import os
from pytest import mark, raises
import shutil
from syndot.utils.map_file import read_map_file, get_map_info, write_map_file
from tests.conftest import (paths, labels, targets, MAP_FILE_PATH,
                            valid_labels, valid_targets, reset_environment)


@mark.utils
class TestReadMapFile:

    @mark.genuine
    @given(explicit_map_file_path=booleans())
    @settings(max_examples=100, deadline=None)
    def test_function(self, explicit_map_file_path):
        local_map_file_path = os.path.join(os.getcwd(), 'map.ini')
        if explicit_map_file_path:
            config = read_map_file(map_file_path=MAP_FILE_PATH)
        else:
            shutil.copy2(MAP_FILE_PATH, local_map_file_path)
            config = read_map_file(map_file_path=None)

        assert isinstance(config, ConfigParser)
        assert config.sections() == ['Path', 'Targets']
        assert list(config['Path'].keys()) == ['settings_dir']
        assert isinstance(config['Path']['settings_dir'], str)
        assert config['Path']['settings_dir']
        for param in config['Targets'].values():
            assert isinstance(param, str)
            assert param

        if not explicit_map_file_path:
            os.remove(local_map_file_path)

    @mark.error
    def test_raises_file_not_found_error(self):
        for map_file_path in ['map.ini', 'not_a_file']:
            with raises(FileNotFoundError):
                read_map_file(map_file_path=map_file_path)


@mark.utils
class TestGetMapInfo:

    @mark.genuine
    @given(label=one_of(lists(
               min_size=1,
               max_size=3,
               elements=labels()),
                        none()),
           path=one_of(lists(
               min_size=1,
               max_size=5,
               elements=targets()),
                       none()))
    @settings(max_examples=100, deadline=None)
    def test_function(self, label, path):
        args = Namespace()
        args.label = label
        args.path = path
        config = read_map_file(map_file_path=MAP_FILE_PATH)

        settings_dir, targets_list = get_map_info(config=config, args=args)

        assert isinstance(settings_dir, str)
        assert settings_dir

        assert isinstance(targets_list, list)
        assert targets_list

        for target in targets_list:
            assert isinstance(target, str)
            assert target

    @mark.error
    def test_raises_name_error(self):
        args = Namespace()
        args.label = valid_labels[0] + '_other'
        args.path = None
        config = read_map_file(map_file_path=MAP_FILE_PATH)
        with raises(NameError):
            get_map_info(config=config, args=args)

        args = Namespace()
        args.label = None
        args.path = valid_targets[0] + '_other'
        config = read_map_file(map_file_path=MAP_FILE_PATH)
        with raises(NameError):
            get_map_info(config=config, args=args)


@mark.utils
class TestWriteMapFile:

    @mark.genuine
    @given(path=paths())
    @settings(max_examples=100, deadline=None)
    def test_function(self, path):
        reset_environment()

        config = read_map_file(map_file_path=MAP_FILE_PATH)

        map_file_path = os.path.join(path, 'map.ini')
        os.makedirs(os.path.dirname(map_file_path))
        write_map_file(map_file_path=map_file_path, config=config)

        assert os.path.exists(map_file_path)
        assert os.path.isfile(map_file_path)

        reset_environment()
