from hypothesis import given, settings
from hypothesis.strategies import booleans
import os
from pytest import mark
import shutil
from syndot.utils.file_actions import copy, change_parent_owner
from tests.conftest import paths, TEST_DATA_PATH, SETTINGS_DIR, create_file_or_directory


@mark.utils
class TestCopy:

    @mark.genuine
    @given(source_path = paths(), destination_path = paths(), is_file = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, source_path, destination_path, is_file):
        if source_path != destination_path:
            create_file_or_directory(path = source_path, is_file = is_file)

            copy(source = source_path, destination = destination_path)

            for path in [source_path, destination_path]:
                assert os.path.exists(path)
                if is_file:
                    assert os.path.isfile(path)
                else:
                    assert os.path.isdir(path)
            source_stat = os.stat(source_path)
            destination_stat = os.stat(destination_path)
            assert source_stat.st_uid == destination_stat.st_uid
            assert source_stat.st_gid == destination_stat.st_gid

            shutil.rmtree(TEST_DATA_PATH)


@mark.utils
class TestChangeParentOwner:

    @mark.genuine
    @given(source_path = paths(absolute = True), is_file = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, source_path, is_file):
        destination_path = os.path.join(os.getcwd(), SETTINGS_DIR, *source_path.split(os.path.sep)[1:])
        for path in [source_path, destination_path]:
            create_file_or_directory(path = path, is_file = is_file)

        change_parent_owner(source = source_path, destination = destination_path, settings_dir = SETTINGS_DIR)

        for path in [source_path, destination_path]:
            assert os.path.exists(path)
            if is_file:
                assert os.path.isfile(path)
            else:
                assert os.path.isdir(path)
        source_parent_path = os.path.dirname(source_path)
        destination_parent_path = os.path.dirname(destination_path)
        while source_parent_path != os.getcwd():
            source_parent_stat = os.stat(source_parent_path)
            destination_parent_stat = os.stat(destination_parent_path)
            assert source_parent_stat.st_uid == destination_parent_stat.st_uid
            assert source_parent_stat.st_gid == destination_parent_stat.st_gid
            source_parent_path = os.path.dirname(source_parent_path)
            destination_parent_path = os.path.dirname(destination_parent_path)

        shutil.rmtree(TEST_DATA_PATH)
