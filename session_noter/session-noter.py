import argparse
import configparser

from cli import CLI
import curses_cli


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--curses", help="enables curses interface", action="store_true")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('session-noter.ini')

    print('Welcome to session-noter!\n')

    if args.curses or config['general']['interface'] == "curses":
        curses_cli.main()
    else:
        interface = CLI(config)
