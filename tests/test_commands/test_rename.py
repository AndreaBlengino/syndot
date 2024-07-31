from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings
from hypothesis.strategies import text, characters, booleans
from pytest import mark, raises
from syndot.commands.rename import rename
from syndot.utils.map_file import read_map_file, write_map_file
from tests.conftest import labels, reset_environment
from tests.test_commands.conftest import (
    generate_testing_map_file,
    TEST_MAP_FILE_PATH
)


@mark.commands
class TestRename:

    @mark.genuine
    @given(
        old_label=labels(),
        new_label=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        new_label_already_in_map_file=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_function(
        self,
        old_label,
        new_label,
        new_label_already_in_map_file
    ):
        if old_label != new_label:
            reset_environment()

            args = Namespace()
            args.old_label = old_label
            args.new_label = new_label
            args.mapfile = TEST_MAP_FILE_PATH

            generate_testing_map_file()
            if new_label_already_in_map_file:
                config = read_map_file(map_file_path=TEST_MAP_FILE_PATH)
                current_targets = dict(config['Targets'])
                for label, paths in current_targets.items():
                    current_targets[label] = paths.split()
                current_targets[new_label] = ['/new/label/path']
                current_targets = dict(sorted(current_targets.items()))
                config['Targets'].clear()
                for label, paths in current_targets.items():
                    config['Targets'][label] = '\n' + '\n'.join(paths)
                write_map_file(map_file_path=TEST_MAP_FILE_PATH, config=config)

            config = ConfigParser()
            config.read(TEST_MAP_FILE_PATH)
            labels = list(config['Targets'].keys())
            path_list = []
            for path in config['Targets'].values():
                path_list.extend(path.split())

            assert old_label in labels
            if new_label_already_in_map_file:
                assert new_label in labels
            else:
                assert new_label not in labels

            old_label_paths = config['Targets'][old_label]

            rename(args=args)

            config = ConfigParser()
            config.read(TEST_MAP_FILE_PATH)
            labels = list(config['Targets'].keys())
            path_list = []
            for path in config['Targets'].values():
                path_list.extend(path.split())

            assert old_label not in labels
            assert new_label in labels

            new_label_paths = config['Targets'][new_label]

            if new_label_already_in_map_file:
                assert old_label_paths in new_label_paths
                assert '/new/label/path' in new_label_paths
            else:
                assert old_label_paths == new_label_paths

            reset_environment()

    @mark.error
    @given(
        old_label=labels(),
        new_label=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_raises_key_error(self, old_label, new_label):
        reset_environment()

        args = Namespace()
        args.old_label = old_label + '_other'
        args.new_label = new_label
        args.mapfile = TEST_MAP_FILE_PATH

        generate_testing_map_file()

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        previous_labels = list(config['Targets'].keys())
        previous_path_list = []
        for path in config['Targets'].values():
            previous_path_list.extend(path.split())

        assert old_label not in previous_path_list

        with raises(KeyError):
            rename(args=args)

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        following_labels = list(config['Targets'].keys())
        following_path_list = []
        for path in config['Targets'].values():
            following_path_list.extend(path.split())

        assert old_label not in following_path_list
        assert previous_labels == following_labels
        assert previous_path_list == following_path_list

        reset_environment()

    @mark.error
    @given(label=labels())
    @settings(max_examples=100, deadline=None)
    def test_raises_name_error(self, label):
        reset_environment()

        args = Namespace()
        args.old_label = label
        args.new_label = label
        args.mapfile = TEST_MAP_FILE_PATH

        with raises(NameError):
            rename(args=args)

        reset_environment()
