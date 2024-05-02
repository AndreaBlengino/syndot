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
                                        usage = '%(prog)s [-b | --backup] [-f | --force] [-m | --mapfile] MAPFILE '
                                                '[-t | --target] TARGET',
                                        description = 'Move dotfiles to destination directory and create symlinks to '
                                                      'them')
link_parser.add_argument('-b', '--backup',
                         action = 'store_true',
                         default = False,
                         required = False,
                         help = 'create a backup copy of the original dotfiles')
link_parser.add_argument('-f', '--force',
                         action = 'store_true',
                         default = False,
                         required = False,
                         help = 'force link in case of already existing dotfiles')
link_parser.add_argument('-m', '--mapfile',
                         required = False,
                         help = 'path to the map file')
link_parser.add_argument('-t', '--target',
                         required = False,
                         help = 'path to the target dotfile')


unlink_parser = command_parser.add_parser('unlink',
                                          prog = 'syndot unlink',
                                          usage = '%(prog)s [-f | --force] [-m | --mapfile] MAPFILE '
                                                  '[-t | --target] TARGET',
                                          description = 'Remove dotfiles symlinks and move them to original directory')
unlink_parser.add_argument('-f', '--force',
                           action = 'store_true',
                           default = False,
                           required = False,
                           help = 'force unlink in case of already existing dotfiles')
unlink_parser.add_argument('-m', '--mapfile',
                           required = False,
                           help = 'path to the map file')
unlink_parser.add_argument('-t', '--target',
                           required = False,
                           help = 'path to the target dotfile')


diffuse_parser = command_parser.add_parser('diffuse',
                                           prog = 'syndot diffuse',
                                           usage = '%(prog)s [-f | --force] [-m | --mapfile] MAPFILE '
                                                   '[-t | --target] TARGET',
                                           description = 'Create dotfiles symlinks')
diffuse_parser.add_argument('-f', '--force',
                            action = 'store_true',
                            default = False,
                            required = False,
                            help = 'force diffuse in case of already existing dotfiles')
diffuse_parser.add_argument('-m', '--mapfile',
                            required = False,
                            help = 'path to the map file')
diffuse_parser.add_argument('-t', '--target',
                            required = False,
                            help = 'path to the target dotfile')


add_parser = command_parser.add_parser('add',
                                       prog = 'syndot add',
                                       usage = '%(prog)s [-m | --mapfile] MAPFILE [-t | --target] TARGET',
                                       description = 'Add dotfiles to map file')
add_parser.add_argument('-m', '--mapfile',
                        required = False,
                        help = 'path to the map file')
add_parser.add_argument('-t', '--target',
                        required = True,
                        help = 'path to the target dotfile')


remove_parser = command_parser.add_parser('remove',
                                          prog = 'syndot remove',
                                          usage = '%(prog)s [-m | --mapfile] MAPFILE [-t | --target] TARGET',
                                          description = 'Remove dotfiles from map file')
remove_parser.add_argument('-m', '--mapfile',
                           required = False,
                           help = 'path to the map file')
remove_parser.add_argument('-t', '--target',
                           required = True,
                           help = 'path to the target dotfile')
