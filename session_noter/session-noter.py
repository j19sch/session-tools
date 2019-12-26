import argparse

from cli import CLI
from curses_interface import interface_wrapper
from utils import read_config_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--curses", help="enables curses interface", action="store_true")
    args = parser.parse_args()

    config = read_config_file()

    if args.curses or config['noter']['interface'] == "curses":
        interface_wrapper(config)
    else:
        CLI(config)
