from cli import CLI
from utils import read_config_file


if __name__ == '__main__':
    config = read_config_file()

    print('Welcome to session-noter!\n')

    CLI(config)
