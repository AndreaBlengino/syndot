from argparse import Namespace
from configparser import ConfigParser
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import booleans
from pytest import mark, raises
from syndot.commands.list_ import list_
from tests.conftest import reset_environment, labels
from tests.test_commands.conftest import (
    generate_testing_map_file,
    TEST_MAP_FILE_PATH
)


@mark.commands
class TestList:

    @mark.genuine
    @given(
        directory_arg=booleans(),
        label_arg=booleans(),
        path_arg=booleans(),
        search=labels()
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_print_action(
        self,
        directory_arg,
        label_arg,
        path_arg,
        search,
        capsys
    ):
        reset_environment()

        args = Namespace()
        args.directory = directory_arg
        if label_arg:
            if path_arg:
                args.label = False
                args.path = False
                args.search = search
            else:
                args.label = True
                args.path = False
                args.search = None
        else:
            if path_arg:
                args.label = False
                args.path = True
                args.search = None
            else:
                args.label = False
                args.path = False
                args.search = None
        args.mapfile = TEST_MAP_FILE_PATH
        generate_testing_map_file()

        list_(args=args)
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output

        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        settings_dir = config['Path']['settings_dir']
        label_list = config['Targets'].keys()
        path_list = []
        for path in config['Targets'].values():
            path_list.extend(path.split())
        search_path_list = config['Targets'][search].split()

        if directory_arg:
            assert "Settings directory:" in printed_output
            assert settings_dir in printed_output
        else:
            assert "Settings directory:" not in printed_output
            assert settings_dir not in printed_output

        for label in label_list:
            if not args.path:
                assert label in printed_output
            else:
                if args.label and search == label:
                    assert label in printed_output
                else:
                    assert label not in printed_output

        for path in path_list:
            if not args.label:
                assert path in printed_output
            else:
                if args.path and path in search_path_list:
                    assert path in printed_output
                else:
                    assert path not in printed_output

        reset_environment()

    @mark.error
    def test_raises_name_error(self):
        reset_environment()

        args = Namespace()
        args.directory = False
        args.label = False
        args.path = False
        args.search = 'label_not_in_map_file'
        args.mapfile = TEST_MAP_FILE_PATH
        generate_testing_map_file()

        with raises(NameError):
            list_(args=args)

        reset_environment()
