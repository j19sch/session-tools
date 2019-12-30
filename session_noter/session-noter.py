from session_noter.core.cli import CLI
from session_noter.core.utils import read_config_file


if __name__ == "__main__":
    config = read_config_file()

    CLI(config)
