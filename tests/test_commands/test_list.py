from argparse import Namespace
from configparser import ConfigParser
from pytest import mark
import shutil
from syndot.commands import list_
from tests.test_commands.conftest import generate_testing_map_file, TEST_MAP_FILE_PATH, TEST_DATA_PATH


@mark.commands
class TestList:

    @mark.genuine
    def test_print_action(self, capsys):

        args = Namespace()
        args.mapfile = TEST_MAP_FILE_PATH
        generate_testing_map_file()

        list_(args = args)
        printed_output = capsys.readouterr().out

        assert isinstance(printed_output, str)
        assert printed_output
        config = ConfigParser()
        config.read(TEST_MAP_FILE_PATH)
        settings_dir = config['Path']['settings_dir']
        target_directories = config['Targets']['directories'].split()
        target_files = config['Targets']['files'].split()
        targets = [*target_directories, *target_files]
        for target in targets:
            assert target in printed_output
        assert "Settings directory:" in printed_output
        assert settings_dir in printed_output

        shutil.rmtree(TEST_DATA_PATH)
