import os
from syndot import commands
from syndot.parser import parser
from syndot import utils


DEFAULT_DESTINATION = '~/Settings'
MAP_TEMPLATE_PATH = os.path.join('..', 'templates', 'map.ini')

args = parser.parse_args()


if args.command == 'init':
    destination = os.path.expanduser(args.path if args.path is not None else DEFAULT_DESTINATION)
    if os.path.exists(destination):
        raise ValueError(f"Destination directory {destination} already exists.")
    os.mkdir(destination)

    config = utils.read_map_file(MAP_TEMPLATE_PATH)
    config['Paths']['destination'] = destination

    utils.write_map_file(map_file_path = os.path.join(destination, 'map.ini'), config = config)

elif args.command == 'link':
    source, destination, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile))

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if os.path.exists(source_target_path):
            if not os.path.islink(source_target_path):
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
                                                                target_is_source = False,
                                                                command = args.command)
                        force_link = utils.prompt_question(question = question, default = 'y')
                        if force_link:
                            utils.remove(path = destination_target_path)
                            commands.link(source_target_path = source_target_path,
                                          destination_target_path = destination_target_path,
                                          backup = args.backup)
            else:
                print(f"Skipping source {source_target_path} because is a symlink")
        else:
            print(f"Skipping missing source {source_target_path}")

elif args.command == 'unlink':
    source, destination, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile))

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if os.path.exists(destination_target_path):
            commands.unlink(source_target_path = source_target_path, destination_target_path = destination_target_path)
        else:
            raise FileNotFoundError(f"Missing {destination_target_path} in destination directory.")

elif args.command == 'diffuse':
    source, destination, targets = utils.get_map_info(config = utils.read_map_file(map_file_path = args.mapfile))

    for target in targets:
        source_target_path, destination_target_path = utils.compose_target_paths(source = source,
                                                                                 destination = destination,
                                                                                 target = target)
        if not os.path.exists(source_target_path):
            if os.path.exists(destination_target_path):
                commands.diffuse(source_target_path = source_target_path,
                                 destination_target_path = destination_target_path)
            else:
                raise FileNotFoundError(f"Missing {destination_target_path} in destination directory.")
        else:
            if args.force:
                utils.remove(path = source_target_path)
                commands.diffuse(source_target_path = source_target_path,
                                 destination_target_path = destination_target_path)
            else:
                question = utils.compose_force_question(target_path = destination_target_path,
                                                        target_is_source = True,
                                                        command = args.command)
                force_diffuse = utils.prompt_question(question = question, default = 'y')
                if force_diffuse:
                    utils.remove(path = source_target_path)
                    commands.diffuse(source_target_path = source_target_path,
                                     destination_target_path = destination_target_path)

elif args.command == 'add':
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')

    target = args.target
    if not os.path.exists(target):
        raise OSError(f"Target {target} not found.")

    config = utils.read_map_file(map_file_path = map_file_path)
    current_targets = []
    if os.path.isfile(target):
        current_targets = config['Targets']['files'].split()
    elif os.path.isdir(target):
        current_targets = config['Targets']['directories'].split()

    relative_target_path = os.path.expanduser(target).replace(os.path.expanduser(config['Paths']['source']), '')[1:]
    current_targets.append(relative_target_path)
    current_targets.sort()

    if os.path.isfile(target):
        config['Targets']['files'] = '\n' + '\n'.join(current_targets)
    elif os.path.isdir(target):
        config['Targets']['directories'] = '\n' + '\n'.join(current_targets)

    utils.write_map_file(map_file_path = map_file_path, config = config)

elif args.command == 'remove':
    map_file_path = os.path.expanduser(args.mapfile if args.mapfile is not None else 'map.ini')

    config = utils.read_map_file(map_file_path = map_file_path)
    current_files = config['Targets']['files'].split()
    current_directories = config['Targets']['directories'].split()
    target = args.target
    if target in current_files:
        current_files.remove(target)
        config['Targets']['files'] = '\n' + '\n'.join(current_files)
    elif target in current_directories:
        current_directories.remove(target)
        config['Targets']['directories'] = '\n' + '\n'.join(current_directories)
    else:
        print(f"Target {target} not found in map file")

    utils.write_map_file(map_file_path = map_file_path, config = config)
