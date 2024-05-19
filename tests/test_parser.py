from hypothesis import given, settings
from hypothesis.strategies import one_of, none, booleans, text, characters
from pytest import mark
from syndot.parser import parser
from tests.conftest import paths


@mark.utils
class TestParser:

    @mark.genuine
    @given(path = one_of(paths(), none()))
    @settings(max_examples = 100, deadline = None)
    def test_init(self, path):
        input_arguments = ['init']
        if path:
            input_arguments.extend(['-p', path])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'init'
        if path:
            assert parsed_arguments.path == path
        else:
            assert parsed_arguments.path is None

    @mark.genuine
    @given(backup = booleans(),
           exact = booleans(),
           map_file_path = one_of(paths(), none()),
           target_path_start = one_of(text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)),
                                      none()))
    @settings(max_examples = 100, deadline = None)
    def test_link(self, backup, exact, map_file_path, target_path_start):
        input_arguments = ['link']
        if backup:
            input_arguments.append('-b')
        if exact:
            input_arguments.append('-e')
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if target_path_start:
            input_arguments.append(target_path_start)
        else:
            input_arguments.append('--all')

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'link'
        if backup:
            assert parsed_arguments.backup
        else:
            assert not parsed_arguments.backup
        if exact:
            assert parsed_arguments.exact
        else:
            assert not parsed_arguments.exact
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        if target_path_start:
            assert parsed_arguments.TARGET_PATH_START == target_path_start
            assert not parsed_arguments.all
        else:
            assert parsed_arguments.TARGET_PATH_START is None
            assert parsed_arguments.all

    @mark.genuine
    @given(exact = booleans(),
           map_file_path = one_of(paths(), none()),
           target_path_start = one_of(text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)),
                                      none()))
    @settings(max_examples = 100, deadline = None)
    def test_unlink(self, exact, map_file_path, target_path_start):
        input_arguments = ['unlink']
        if exact:
            input_arguments.append('-e')
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if target_path_start:
            input_arguments.append(target_path_start)
        else:
            input_arguments.append('--all')

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'unlink'
        if exact:
            assert parsed_arguments.exact
        else:
            assert not parsed_arguments.exact
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        if target_path_start:
            assert parsed_arguments.TARGET_PATH_START == target_path_start
            assert not parsed_arguments.all
        else:
            assert parsed_arguments.TARGET_PATH_START is None
            assert parsed_arguments.all

    @mark.genuine
    @given(exact = booleans(),
           map_file_path = one_of(paths(), none()),
           target_path_start = one_of(text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)),
                                      none()))
    @settings(max_examples = 100, deadline = None)
    def test_diffuse(self, exact, map_file_path, target_path_start):
        input_arguments = ['diffuse']
        if exact:
            input_arguments.append('-e')
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if target_path_start:
            input_arguments.append(target_path_start)
        else:
            input_arguments.append('--all')

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'diffuse'
        if exact:
            assert parsed_arguments.exact
        else:
            assert not parsed_arguments.exact
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        if target_path_start:
            assert parsed_arguments.TARGET_PATH_START == target_path_start
            assert not parsed_arguments.all
        else:
            assert parsed_arguments.TARGET_PATH_START is None
            assert parsed_arguments.all

    @mark.genuine
    @given(map_file_path = one_of(paths(), none()),
           target_path = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)))
    @settings(max_examples = 100, deadline = None)
    def test_add(self, map_file_path, target_path):
        input_arguments = ['add']
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        input_arguments.append(target_path)

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'add'
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        assert parsed_arguments.TARGET_PATH == target_path

    @mark.genuine
    @given(map_file_path = one_of(paths(), none()),
           target_path = text(min_size = 5, max_size = 10, alphabet = characters(min_codepoint = 97, max_codepoint = 122)))
    @settings(max_examples = 100, deadline = None)
    def test_remove(self, map_file_path, target_path):
        input_arguments = ['remove']
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        input_arguments.append(target_path)

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'remove'
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        assert parsed_arguments.TARGET_PATH == target_path

    @mark.genuine
    @given(map_file_path = one_of(paths(), none()))
    @settings(max_examples = 100, deadline = None)
    def test_list(self, map_file_path):
        input_arguments = ['list']
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'list'
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
