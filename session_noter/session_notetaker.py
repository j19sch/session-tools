from session_noter.core.cli import CLI
from session_noter.core.utils import read_config_file


def main():
    config = read_config_file()

    CLI(config)
