import sys
import yaml


def read_config_file():
    with open('./config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    return config


def validate_config_file(config_file):
    commands = []
    for note_type in config_file['note_types']:
        if config_file['note_types'][note_type]['command'] in commands:
            sys.exit(f"Duplicate command in config.yml: {note_type}")
        else:
            commands.append(config_file['note_types'][note_type]['command'])
