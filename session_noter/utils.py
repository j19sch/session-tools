import os
import sys
import yaml


def read_config_file():
    path_to_this_file = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(path_to_this_file, 'config.yml'), 'r') as config_file:
        config = yaml.safe_load(config_file)

    validate_config_file(config)

    return config


def validate_config_file(config):
    commands = []
    for note_type in config['note_types']:
        if config['note_types'][note_type]['command'] in commands:
            sys.exit(f"Duplicate command in config.yml: {note_type}")
        else:
            commands.append(config['note_types'][note_type]['command'])
