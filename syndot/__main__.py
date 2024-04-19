from argparse import ArgumentParser
from configparser import ConfigParser
import os
from syndot import commands
from syndot import utils


parser = ArgumentParser()
command_parser = parser.add_subparsers(dest = 'command')

init_parser = command_parser.add_parser('init')
init_parser.add_argument('-p', '--path', required = False)

link_parser = command_parser.add_parser('link')
link_parser.add_argument('-m', '--mapfile', required = False)
link_parser.add_argument('-b', '--backup', action = 'store_true', default = False, required = False)
link_parser.add_argument('-f', '--force', action = 'store_true', default = False, required = False)

unlink_parser = command_parser.add_parser('unlink')
unlink_parser.add_argument('-m', '--mapfile', required = False)

diffuse_parser = command_parser.add_parser('diffuse')
diffuse_parser.add_argument('-m', '--mapfile', required = False)
diffuse_parser.add_argument('-f', '--force', action = 'store_true', default = False, required = False)

args = parser.parse_args()


DEFAULT_DESTINATION = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join('..', 'templates', 'map.ini')


if args.command == 'init':
    destination = os.path.expanduser(args.path if args.path is not None else DEFAULT_DESTINATION)
    if os.path.exists(destination):
        raise ValueError(f"Destination directory {destination} already exists.")
    os.mkdir(destination)

    config = ConfigParser()
    config.read(MAP_TEMPLATE_PATH)
    config['Paths']['destination'] = destination

    with open(os.path.join(destination, 'map.ini'), 'w') as map_file:
        config.write(map_file)

elif args.command == 'link':
    source, destination, targets = utils.read_map_file(map_file = args.mapfile)

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if os.path.exists(source_target_path):
            if not os.path.exists(destination_target_path):
                commands.link(source_target_path = source_target_path,
                              destination_target_path = destination_target_path,
                              backup = args.backup)
            else:
                if args.force:
                    utils.remove(path = destination_target_path)
                    commands.link(source_target_path = source_target_path,
                                  destination_target_path = destination_target_path,
                                  backup = args.backup)
                else:
                    question = utils.compose_force_question(target_path = destination_target_path,
                                                            target = target,
                                                            target_is_source = False,
                                                            command = args.command)
                    force_link = utils.prompt_question(question = question, default = 'y')
                    if force_link:
                        utils.remove(path = destination_target_path)
                        commands.link(source_target_path = source_target_path,
                                      destination_target_path = destination_target_path,
                                      backup = args.backup)
        else:
            print(f"Skipping missing source {source_target_path}.")

elif args.command == 'unlink':
    source, destination, targets = utils.read_map_file(map_file = args.mapfile)

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        commands.unlink(source_target_path = source_target_path, destination_target_path = destination_target_path)

elif args.command == 'diffuse':
    source, destination, targets = utils.read_map_file(map_file = args.mapfile)

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if not os.path.exists(source_target_path):
            commands.diffuse(source_target_path = source_target_path, destination_target_path = destination_target_path)
        else:
            if args.force:
                utils.remove(path = source_target_path)
                commands.diffuse(source_target_path = source_target_path,
                                 destination_target_path = destination_target_path)
            else:
                question = utils.compose_force_question(target_path = destination_target_path,
                                                        target = target,
                                                        target_is_source = True,
                                                        command = args.command)
                force_diffuse = utils.prompt_question(question = question, default = 'y')
                if force_diffuse:
                    utils.remove(path = source_target_path)
                    commands.diffuse(source_target_path = source_target_path,
                                     destination_target_path = destination_target_path)
