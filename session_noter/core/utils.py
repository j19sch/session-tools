import os
import sys
import yaml


def read_config_file() -> dict:
    path_to_this_file = os.path.dirname(os.path.realpath(__file__))

    # ToDo: determine path to file properly
    with open(os.path.join(path_to_this_file, "..", "config.yml"), "r") as config_file:
        config = yaml.safe_load(config_file)

    validate_config_file(config)

    return config


def validate_config_file(config: dict):
    commands = []
    for _ in config["note_types"]:
        if _["command"] in commands:
            sys.exit(f"Duplicate command in config.yml: {_['type']}")
        else:
            commands.append(_["command"])
