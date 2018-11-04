import csv
import datetime
import mss


class Noter:
    def __init__(self, tester, charter, duration, file):
        # ToDo: dynamic adding of attributes
        self._notes = []
        self._file = file
        self._writer = csv.writer(self._file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        self._tester = tester
        self.add_note('tester', tester)

        self._charter = charter
        self.add_note('charter', charter)

        self._duration = duration
        self.add_note('duration', duration)

        self._session_start = None

    def start_session(self):
        now = datetime.datetime.now()
        self._session_start = now
        self.add_note('session start', '', now)

    def calculate_elapsed_seconds(self):
        return (datetime.datetime.now() - self._session_start).total_seconds()

    def add_note(self, note_type, content, timestamp=None):
        timestamp = datetime.datetime.now() if timestamp is None else timestamp
        self._notes.append({'timestamp': timestamp, 'type': note_type, 'content': content})
        self._writer.writerow([timestamp.strftime('%Y-%m-%dT%H:%M:%S'), note_type, content])
        self._file.flush()

    def all_notes(self):
        return self._notes

    def all_notes_of_type(self, note_type):
        return [note for note in self._notes if note['type'] == note_type]

    def n_latest_notes(self, number):
        return self._notes[-number:]

    def take_screenshot(self):
        timestamp = datetime.datetime.now()
        with mss.mss() as sct:
            sct.shot(output='{}.png'.format(timestamp.strftime('%Y-%m-%dT%H%M%S')))

        self.add_note('capture', '', timestamp=timestamp)
