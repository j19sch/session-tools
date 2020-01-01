import os
import sys
from typing import List

import yaml


def read_config_file():  # type: ignore
    path_to_this_file = os.path.dirname(os.path.realpath(__file__))

    # ToDo: determine path to file properly
    with open(os.path.join(path_to_this_file, "..", "config.yml"), "r") as config_file:
        config = yaml.safe_load(config_file)

    validate_config_file(config)

    return config


def validate_config_file(config: dict) -> None:
    commands: List[str] = []
    for _ in config["note_types"]:
        if _["command"] in commands:
            sys.exit(f"Duplicate command in config.yml: {_['type']}")
        else:
            commands.append(_["command"])
