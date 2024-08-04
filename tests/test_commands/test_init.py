from argparse import Namespace
from hypothesis import given, settings
import os
from pytest import mark, raises
from syndot.commands.init import init
from tests.conftest import paths, create_file_or_directory, reset_environment


@mark.commands
class TestInit:

    @mark.genuine
    @given(path=paths())
    @settings(max_examples=100, deadline=None)
    def test_function(self, path):
        reset_environment()

        args = Namespace()
        args.path = path

        assert not os.path.exists(path)

        init(args=args)

        assert os.path.exists(path)
        content = os.listdir(path)
        assert len(content) == 1
        assert 'map.ini' in content

        reset_environment()

    @mark.error
    @given(path=paths())
    @settings(max_examples=100, deadline=None)
    def test_raises_value_error(self, path):
        reset_environment()

        args = Namespace()
        args.path = path
        create_file_or_directory(path=path, is_file=False)

        assert os.path.exists(path)
        assert os.path.isdir(path)

        with raises(ValueError):
            init(args=args)

        assert os.path.exists(path)
        assert os.path.isdir(path)
        assert not os.listdir(path)

        reset_environment()
