from session_tools.core.cli import CLI
from session_tools.core.utils import read_config_file


def main():
    config = read_config_file()

    CLI(config)
