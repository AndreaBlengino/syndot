from argparse import ArgumentParser


parser = ArgumentParser(prog = 'syndot',
                        usage = '%(prog)s [-v | --version] [-h | --help] <command> [<args>]',
                        description = 'Manage symlinks to dotfiles')
parser.add_argument('-v', '--version',
                    action = 'version',
                    version = '%(prog)s 0.0.0')
command_parser = parser.add_subparsers(dest = 'command')


init_parser = command_parser.add_parser('init',
                                        prog = 'syndot init',
                                        usage = '%(prog)s [-p | --path]',
                                        description = 'Initialize destination directory in which to store dotfiles')
init_parser.add_argument('-p', '--path',
                         required = False,
                         help = 'path to the destination directory')


link_parser = command_parser.add_parser('link',
                                        prog = 'syndot link',
                                        usage = '%(prog)s [-b | --backup] [-m | --mapfile] MAPFILE '
                                                '[[-a | --all] | TARGET_PATH_START]',
                                        description = 'Move dotfiles to destination directory and create symlinks to '
                                                      'them')
link_parser.add_argument('-b', '--backup',
                         action = 'store_true',
                         default = False,
                         required = False,
                         help = 'create a backup copy of the original dotfiles')
link_parser.add_argument('-m', '--mapfile',
                         required = False,
                         help = 'path to the map file')
link_targets = link_parser.add_mutually_exclusive_group(required = True)
link_targets.add_argument('TARGET_PATH_START',
                          nargs = '?',
                          help = 'targets starting path')
link_targets.add_argument('-a', '--all',
                          action = 'store_true',
                          default = False,
                          required = False,
                          help = 'select all targets in the map file')


unlink_parser = command_parser.add_parser('unlink',
                                          prog = 'syndot unlink',
                                          usage = '%(prog)s [-m | --mapfile] MAPFILE '
                                                  '[[-a | --all] | TARGET_PATH_START]',
                                          description = 'Remove dotfiles symlinks and move them to original directory')
unlink_parser.add_argument('-m', '--mapfile',
                           required = False,
                           help = 'path to the map file')
unlink_targets = unlink_parser.add_mutually_exclusive_group(required = True)
unlink_targets.add_argument('TARGET_PATH_START',
                            nargs = '?',
                            help = 'targets starting path')
unlink_targets.add_argument('-a', '--all',
                            action = 'store_true',
                            default = False,
                            required = False,
                            help = 'select all targets in the map file')


diffuse_parser = command_parser.add_parser('diffuse',
                                           prog = 'syndot diffuse',
                                           usage = '%(prog)s [-m | --mapfile] MAPFILE '
                                                   '[[-a | --all] | TARGET_PATH_START]',
                                           description = 'Create dotfiles symlinks')
diffuse_parser.add_argument('-m', '--mapfile',
                            required = False,
                            help = 'path to the map file')
diffuse_targets = diffuse_parser.add_mutually_exclusive_group(required = True)
diffuse_targets.add_argument('TARGET_PATH_START',
                             nargs = '?',
                             help = 'targets starting path')
diffuse_targets.add_argument('-a', '--all',
                             action = 'store_true',
                             default = False,
                             required = False,
                             help = 'select all targets in the map file')


add_parser = command_parser.add_parser('add',
                                       prog = 'syndot add',
                                       usage = '%(prog)s [-m | --mapfile] MAPFILE TARGET_PATH',
                                       description = 'Add dotfiles to map file')
add_parser.add_argument('-m', '--mapfile',
                        required = False,
                        help = 'path to the map file')
add_parser.add_argument('TARGET_PATH',
                        help = 'path to the target dotfile')


remove_parser = command_parser.add_parser('remove',
                                          prog = 'syndot remove',
                                          usage = '%(prog)s [-m | --mapfile] MAPFILE TARGET_PATH',
                                          description = 'Remove dotfiles from map file')
remove_parser.add_argument('-m', '--mapfile',
                           required = False,
                           help = 'path to the map file')
remove_parser.add_argument('TARGET_PATH',
                           help = 'path to the target dotfile')
