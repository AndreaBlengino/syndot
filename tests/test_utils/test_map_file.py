from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings
from hypothesis.strategies import booleans, one_of, none
import os
from pytest import mark, raises
import shutil
from syndot.utils.map_file import read_map_file, get_map_info, write_map_file
from tests.conftest import paths, targets, MAP_FILE_PATH, TEST_DATA_PATH


@mark.utils
class TestReadMapFile:

    @mark.genuine
    @given(explicit_map_file_path = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, explicit_map_file_path):
        local_map_file_path = os.path.join(os.getcwd(), 'map.ini')
        if explicit_map_file_path:
            config = read_map_file(map_file_path = MAP_FILE_PATH)
        else:
            shutil.copy2(MAP_FILE_PATH, local_map_file_path)
            config = read_map_file(map_file_path = None)

        assert isinstance(config, ConfigParser)
        assert config.sections() == ['Path', 'Targets']
        assert list(config['Path'].keys()) == ['settings_dir']
        assert list(config['Targets'].keys()) == ['directories', 'files']
        for param in [config['Path']['settings_dir'], config['Targets']['directories'], config['Targets']['files']]:
            assert isinstance(param, str)
            assert param

        if not explicit_map_file_path:
            os.remove(local_map_file_path)

    @mark.error
    def test_raises_file_not_found_error(self):
        for map_file_path in ['map.ini', 'not_a_file']:
            with raises(FileNotFoundError):
                read_map_file(map_file_path = map_file_path)


@mark.utils
class TestGetMapInfo:

    @mark.genuine
    @given(exact_match = booleans(), target_path = one_of(targets(), none()), truncate_path = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, exact_match, target_path, truncate_path):
        args = Namespace()
        args.all = target_path is None
        args.exact = exact_match
        truncated_target_path = os.path.split(target_path)[0] if truncate_path and target_path is not None else target_path
        args.TARGET_PATH_START = truncated_target_path
        config = read_map_file(map_file_path = MAP_FILE_PATH)

        settings_dir, targets_list = get_map_info(config = config, args = args)

        assert isinstance(settings_dir, str)
        assert settings_dir

        assert isinstance(targets_list, list)
        if target_path is None and args.all:
            assert targets_list
            assert len(targets_list) > 1
        else:
            if exact_match:
                if truncate_path:
                    assert not targets_list
                else:
                    assert targets_list
                    assert truncated_target_path in targets_list
                    assert len(targets_list) == 1
            else:
                assert targets_list
                assert all([target.startswith(truncated_target_path) for target in targets_list])
        for target in targets_list:
            assert isinstance(target, str)
            assert target


@mark.utils
class TestWriteMapFile:

    @mark.genuine
    @given(path = paths())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, path):
        config = read_map_file(map_file_path = MAP_FILE_PATH)

        map_file_path = os.path.join(path, 'map.ini')
        os.makedirs(os.path.dirname(map_file_path))
        write_map_file(map_file_path = map_file_path, config = config)

        assert os.path.exists(map_file_path)
        assert os.path.isfile(map_file_path)

        shutil.rmtree(TEST_DATA_PATH)
