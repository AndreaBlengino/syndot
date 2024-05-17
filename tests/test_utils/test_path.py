from hypothesis import given, settings
from hypothesis.strategies import booleans, one_of, none
import os
from pytest import mark
import shutil
from syndot.utils.path import generate_backup_path, split_path, expand_home_path, compose_target_paths
from tests.conftest import paths, usernames, TEST_DATA_PATH, SETTINGS_DIR


@mark.utils
class TestGenerateBackupPath:

    @mark.genuine
    @given(path = paths(), is_file = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, path, is_file):
        if is_file:
            os.makedirs(os.path.dirname(path))
            with open(path, 'w') as file:
                file.write('')
        else:
            os.makedirs(path)

        backup_path = generate_backup_path(path = path)

        assert isinstance(backup_path, str)
        assert backup_path
        if is_file:
            assert backup_path.endswith('.bak')
        else:
            assert backup_path.endswith('_bak')
        assert path == backup_path[:-4]

        shutil.rmtree(TEST_DATA_PATH)


@mark.utils
class TestSplitPath:

    @mark.genuine
    @given(path = paths())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, path):
        splitted = split_path(path = path)

        assert isinstance(splitted, list)
        assert splitted
        assert len(splitted) == path.count(os.sep)
        assert path.endswith(os.sep.join(splitted))


@mark.utils
class TestExpandHomePath:

    @mark.genuine
    @given(path = paths(), sudo_user = one_of(usernames(), none()), add_home = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, path, sudo_user, add_home):
        if sudo_user:
            os.environ['SUDO_USER'] = sudo_user
        if add_home:
            path = os.path.join('~', path)

        expanded_path = expand_home_path(path = path)

        assert isinstance(expanded_path, str)
        assert expanded_path
        if add_home:
            if sudo_user:
                assert expanded_path.startswith(os.path.join(os.sep, 'home', sudo_user))
            else:
                assert expanded_path.startswith(os.path.join(os.sep, 'home'))
        else:
            assert expanded_path == path


class TestComposeTargetPaths:

    @mark.genuine
    @given(target_path = paths(absolute = True), add_home = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_function(self, target_path, add_home):
        if add_home:
            target_path = os.path.join('~', target_path)

        system_target_path, settings_target_path = compose_target_paths(settings_dir = SETTINGS_DIR,
                                                                        target = target_path)

        for path in [system_target_path, settings_target_path]:
            assert isinstance(path, str)
            assert path
        if add_home:
            assert system_target_path.startswith(os.path.join(os.sep, 'home'))
        else:
            assert system_target_path == target_path
        assert settings_target_path.startswith(SETTINGS_DIR)
        assert settings_target_path.endswith(target_path)
