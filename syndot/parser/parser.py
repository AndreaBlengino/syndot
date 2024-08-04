from argparse import ArgumentParser, HelpFormatter, SUPPRESS, _SubParsersAction
from operator import attrgetter
from syndot.version import __version__


class GeneralFormatter(HelpFormatter):

    def __init__(self, prog):
        super().__init__(prog, max_help_position=20, width=80)

    def _iter_indented_subactions(self, action):
        if hasattr(action, '_get_subactions'):
            get_subactions = action._get_subactions
            if isinstance(action, _SubParsersAction):
                for subaction in sorted(
                    get_subactions(),
                    key=lambda x: x.dest
                ):
                    yield subaction
            else:
                for subaction in get_subactions():
                    yield subaction

    def _format_action(self, action):
        result = super()._format_action(action)
        if isinstance(action, _SubParsersAction):
            return "%*s%s" % (self._current_indent, '', result.lstrip())
        return result

    def _format_action_invocation(self, action):
        if isinstance(action, _SubParsersAction):
            return ""
        return super()._format_action_invocation(action)


class CommandFormatter(HelpFormatter):

    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=80)

    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter('option_strings'))
        super(CommandFormatter, self).add_arguments(actions)

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string


parser = ArgumentParser(
    prog='syndot',
    usage="%(prog)s <COMMAND> [<OPTIONS>...]",
    description="Manage symlinks to dotfiles",
    epilog="Config file path: ~/.config/syndot",
    add_help=False,
    formatter_class=GeneralFormatter
)

parser.add_argument(
    '-h', '--help',
    action='help',
    default=SUPPRESS,
    help="Show this help message and exit"
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=f"%(prog)s {__version__}",
    help="Show program\"s version number and exit"
)

command_parser = parser.add_subparsers(
    dest='command',
    title='commands'
)
