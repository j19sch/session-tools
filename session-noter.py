import sys
import configparser

from cli import CLI, add_note_type
from noter import Noter

if __name__ == '__main__':
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

            for abbreviation in config['note_types']:
                add_note_type(CLI, abbreviation, config['note_types'][abbreviation])

            cli = CLI(noter)
            cli.cmdloop()
        else:
            sys.exit()
