import argparse

from cli import CLI
import curses_interface
from utils import read_config_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--curses", help="enables curses interface", action="store_true")
    args = parser.parse_args()

    config = read_config_file()

    if args.curses or config['noter']['interface'] == "curses":
        curses_interface.main()
    else:
        interface = CLI(config)
