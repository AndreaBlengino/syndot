from hypothesis import given, settings
from hypothesis.strategies import booleans
import os
from pytest import mark
import shutil
from syndot.utils.path import generate_backup_path
from tests.conftest import paths, TEST_DATA_PATH


@mark.utils
class TestGenerateBackupPath:

    @mark.genuine
    @given(path = paths(), is_file = booleans())
    @settings(max_examples = 10, deadline = None)
    def test_function(self, path, is_file):
        if is_file:
            os.makedirs(os.path.dirname(path))
            with open(path, 'w') as file:
                file.write('')
        else:
            os.makedirs(path)

        backup_path = generate_backup_path(path = path)

        if is_file:
            assert backup_path.endswith('.bak')
        else:
            assert backup_path.endswith('_bak')
        assert path == backup_path[:-4]

        shutil.rmtree(TEST_DATA_PATH)
