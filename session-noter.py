import argparse
import configparser
import sys

from cli import CLI, add_note_type
import curses_cli
from noter import Noter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--curses", help="enables curses interface", action="store_true")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('session-noter.ini')

    print('Welcome to session-noter!')

    with open('noter.csv', 'w', newline='') as csvfile:
        tester = input('tester: ')
        charter = input('charter: ')
        duration = 10

        noter = Noter(tester, charter, duration, csvfile)

        ready_to_go = input('Press Enter to start, any other key to abort. ')
        if ready_to_go == '':
            noter.start_session()

            if args.curses or config['general']['interface'] == "curses":
                curses_cli.main()
            else:
                # ToDo: put loop in function, but requires solution for late binding closures
                for abbreviation in config['note_types']:
                    add_note_type(CLI, abbreviation, config['note_types'][abbreviation])

                cli = CLI(noter)
                cli.cmdloop()
        else:
            sys.exit()
