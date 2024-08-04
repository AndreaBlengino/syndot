from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import (
    one_of,
    none,
    booleans,
    text,
    characters,
    sampled_from,
    lists
)
from pytest import mark, raises
from syndot.parser.parser import parser
from tests.conftest import paths


@mark.parsers
class TestParser:

    @mark.genuine
    @given(path=one_of(paths(), none()))
    @settings(max_examples=100, deadline=None)
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
    @given(
        backup=booleans(),
        label_list=one_of(
            lists(
                min_size=1,
                max_size=5,
                elements=text(
                    min_size=5,
                    max_size=10,
                    alphabet=characters(min_codepoint=97, max_codepoint=122)
                )
            ),
            none()
        ),
        path_list=one_of(
            lists(
                min_size=1,
                max_size=5,
                elements=text(
                    min_size=5,
                    max_size=10,
                    alphabet=characters(min_codepoint=97, max_codepoint=122)
                )
            ),
            none()
        ),
        map_file_path=one_of(paths(), none()),
        no_confirm=booleans(),
        interactive=booleans(),
        start=one_of(
            text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            none()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_link(
        self,
        backup,
        label_list,
        path_list,
        map_file_path,
        no_confirm,
        interactive,
        start
    ):
        input_arguments = ['link']
        if backup:
            input_arguments.append('-b')
        if label_list:
            if path_list:
                if interactive:
                    input_arguments.extend(['-i'])
            else:
                input_arguments.extend(['-l', *label_list])
        else:
            if path_list:
                input_arguments.extend(['-p', *path_list])
            else:
                if interactive:
                    input_arguments.extend(['-i'])
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if no_confirm:
            input_arguments.extend(['-n'])
        if start:
            input_arguments.extend(['-s', start])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'link'
        assert parsed_arguments.backup == backup
        if label_list:
            if path_list:
                assert parsed_arguments.label is None
                assert parsed_arguments.path is None
                assert parsed_arguments.interactive == interactive
            else:
                assert parsed_arguments.label == label_list
                assert parsed_arguments.path is None
                assert not parsed_arguments.interactive
        else:
            if path_list:
                assert parsed_arguments.label is None
                assert parsed_arguments.path == path_list
                assert not parsed_arguments.interactive
            else:
                assert parsed_arguments.label is None
                assert parsed_arguments.path is None
                assert parsed_arguments.interactive == interactive
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        assert parsed_arguments.no_confirm == no_confirm
        if start:
            assert parsed_arguments.start == start
        else:
            assert parsed_arguments.start is None

    @mark.genuine
    @given(
        label_list=one_of(
            lists(
               min_size=1,
               max_size=5,
               elements=text(
                   min_size=5,
                   max_size=10,
                   alphabet=characters(min_codepoint=97, max_codepoint=122)
                )
            ),
            none()
        ),
        path_list=one_of(
            lists(
                min_size=1,
                max_size=5,
                elements=text(
                    min_size=5,
                    max_size=10,
                    alphabet=characters(min_codepoint=97, max_codepoint=122)
                )
            ),
            none()
        ),
        map_file_path=one_of(paths(), none()),
        no_confirm=booleans(),
        interactive=booleans(),
        start=one_of(
            text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            none()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_unlink(
        self,
        label_list,
        path_list,
        map_file_path,
        no_confirm,
        interactive,
        start
    ):
        input_arguments = ['unlink']
        if label_list:
            if path_list:
                if interactive:
                    input_arguments.extend(['-i'])
            else:
                input_arguments.extend(['-l', *label_list])
        else:
            if path_list:
                input_arguments.extend(['-p', *path_list])
            else:
                if interactive:
                    input_arguments.extend(['-i'])
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if no_confirm:
            input_arguments.extend(['-n'])
        if start:
            input_arguments.extend(['-s', start])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'unlink'
        if label_list:
            if path_list:
                assert parsed_arguments.label is None
                assert parsed_arguments.path is None
                assert parsed_arguments.interactive == interactive
            else:
                assert parsed_arguments.label == label_list
                assert parsed_arguments.path is None
                assert not parsed_arguments.interactive
        else:
            if path_list:
                assert parsed_arguments.label is None
                assert parsed_arguments.path == path_list
                assert not parsed_arguments.interactive
            else:
                assert parsed_arguments.label is None
                assert parsed_arguments.path is None
                assert parsed_arguments.interactive == interactive
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        assert parsed_arguments.no_confirm == no_confirm
        if start:
            assert parsed_arguments.start == start
        else:
            assert parsed_arguments.start is None

    @mark.genuine
    @given(
        label_list=one_of(
            lists(
               min_size=1,
               max_size=5,
               elements=text(
                   min_size=5,
                   max_size=10,
                   alphabet=characters(min_codepoint=97, max_codepoint=122)
                )
            ),
            none()
        ),
        path_list=one_of(
            lists(
                min_size=1,
                max_size=5,
                elements=text(
                    min_size=5,
                    max_size=10,
                    alphabet=characters(min_codepoint=97, max_codepoint=122)
                )
            ),
            none()
        ),
        map_file_path=one_of(paths(), none()),
        no_confirm=booleans(),
        interactive=booleans(),
        start=one_of(
            text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            none()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_diffuse(
        self,
        label_list,
        path_list,
        map_file_path,
        no_confirm,
        interactive,
        start
    ):
        input_arguments = ['diffuse']
        if label_list:
            if path_list:
                if interactive:
                    input_arguments.extend(['-i'])
            else:
                input_arguments.extend(['-l', *label_list])
        else:
            if path_list:
                input_arguments.extend(['-p', *path_list])
            else:
                if interactive:
                    input_arguments.extend(['-i'])
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if no_confirm:
            input_arguments.extend(['-n'])
        if start:
            input_arguments.extend(['-s', start])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'diffuse'
        if label_list:
            if path_list:
                assert parsed_arguments.label is None
                assert parsed_arguments.path is None
                assert parsed_arguments.interactive == interactive
            else:
                assert parsed_arguments.label == label_list
                assert parsed_arguments.path is None
                assert not parsed_arguments.interactive
        else:
            if path_list:
                assert parsed_arguments.label is None
                assert parsed_arguments.path == path_list
                assert not parsed_arguments.interactive
            else:
                assert parsed_arguments.label is None
                assert parsed_arguments.path is None
                assert parsed_arguments.interactive == interactive
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        assert parsed_arguments.no_confirm == no_confirm
        if start:
            assert parsed_arguments.start == start
        else:
            assert parsed_arguments.start is None

    @given(
        label=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        map_file_path=one_of(paths(), none()),
        path_list=lists(
            min_size=5,
            max_size=10,
            elements=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            )
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_add(self, label, map_file_path, path_list):
        input_arguments = ['add']
        input_arguments.extend(['-l', label])
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        input_arguments.extend(['-p', *path_list])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'add'
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        assert parsed_arguments.label == label
        assert parsed_arguments.path == path_list

    @mark.genuine
    @given(
        label_list=lists(
            min_size=5,
            max_size=10,
            elements=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            )
        ),
        map_file_path=one_of(paths(), none()),
        path_list=lists(
            min_size=5,
            max_size=10,
            elements=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            )
        ),
        arg_is_label=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_remove(self, label_list, map_file_path, path_list, arg_is_label):
        input_arguments = ['remove']
        if arg_is_label:
            input_arguments.extend(['-l', *label_list])
        else:
            input_arguments.extend(['-p', *path_list])
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'remove'
        if arg_is_label:
            assert parsed_arguments.label == label_list
            assert parsed_arguments.path is None
        else:
            assert parsed_arguments.label is None
            assert parsed_arguments.path == path_list
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None

    @mark.genuine
    @given(
        directory=booleans(),
        label=booleans(),
        map_file_path=one_of(paths(), none()),
        path=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_list(self, directory, label, map_file_path, path):
        input_arguments = ['list']
        if directory:
            input_arguments.append('-d')
        if label and not path:
            input_arguments.append('-l')
        if map_file_path:
            input_arguments.extend(['-m', map_file_path])
        if path and not label:
            input_arguments.append('-p')

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'list'
        if directory:
            assert parsed_arguments.directory
        else:
            assert not parsed_arguments.directory
        if label and not path:
            assert parsed_arguments.label
            assert not parsed_arguments.path
        if map_file_path:
            assert parsed_arguments.mapfile == map_file_path
        else:
            assert parsed_arguments.mapfile is None
        if path and not label:
            assert parsed_arguments.path
            assert not parsed_arguments.label
        if not label and not path:
            assert not parsed_arguments.label
            assert not parsed_arguments.path

    @mark.genuine
    @given(
        old_label=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        ),
        new_label=text(
            min_size=5,
            max_size=10,
            alphabet=characters(min_codepoint=97, max_codepoint=122)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_rename(self, old_label, new_label):
        input_arguments = f"rename -o {old_label} -n {new_label}".split()

        parsed_arguments = parser.parse_args(input_arguments)

        assert parsed_arguments.command == 'rename'
        assert parsed_arguments.old_label == old_label
        assert parsed_arguments.new_label == new_label

    @mark.genuine
    @given(abbreviation=booleans())
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_version(self, abbreviation, capsys):
        args = ['-v'] if abbreviation else ['--version']
        with raises(SystemExit):
            parser.parse_args(args=args)
        printed_output = capsys.readouterr().out

        assert printed_output.startswith('syndot')

    @mark.genuine
    @given(abbreviation=booleans())
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_help(self, abbreviation, capsys):
        args = ['-h'] if abbreviation else ['--help']
        with raises(SystemExit):
            parser.parse_args(args=args)
        printed_output = capsys.readouterr().out

        assert printed_output.startswith(
            "usage: syndot <COMMAND> [<OPTIONS>...]"
        )
        assert printed_output.endswith("Config file path: ~/.config/syndot\n")
        assert 'options:' in printed_output
        assert 'commands:' in printed_output
        assert '-h, --help' in printed_output
        assert '-v, --version' in printed_output
        assert 'add' in printed_output
        assert 'diffuse' in printed_output
        assert 'init' in printed_output
        assert 'link' in printed_output
        assert 'list' in printed_output
        assert 'remove' in printed_output
        assert 'rename' in printed_output
        assert 'unlink' in printed_output

    @mark.genuine
    @given(
        command=sampled_from(
            elements=[
                'add',
                'diffuse',
                'init',
                'link',
                'list',
                'remove',
                'unlink'
            ]
        ),
        abbreviation=booleans()
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_command_help(self, command, abbreviation, capsys):
        args = [command]
        if abbreviation:
            args.append('-h')
        else:
            args.append('--help')
        with raises(SystemExit):
            parser.parse_args(args=args)
        printed_output = capsys.readouterr().out

        assert printed_output.startswith(f"usage: syndot {command}")
        assert 'options' in printed_output
        assert '-h, --help' in printed_output
        if command in ['add', 'diffuse', 'link', 'list', 'remove', 'unlink']:
            assert '-m, --mapfile <MAP_FILE>' in printed_output
        if command in ['diffuse', 'link', 'unlink']:
            assert '-l, --label' in printed_output
            assert '-p, --path' in printed_output
        if command == 'init':
            assert '-p, --path <PATH>' in printed_output
        if command == 'link':
            assert '-b, --backup' in printed_output
