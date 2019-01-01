import csv
import datetime
import mss


class Noter:
    def __init__(self, filename, tester, charter, duration):
        self._notes = []
        self._filename = filename

        self._tester = tester
        self._charter = charter
        self._duration = duration

        self._session_start = None

    def __enter__(self):
        self._file = open(self._filename, 'w', newline='')
        self._writer = csv.writer(self._file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.add_note('duration', self._tester)
        self.add_note('duration', self._charter)
        self.add_note('duration', self._duration)
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self._file.close()

    @property
    def duration(self):
        try:
            return self._duration
        except AttributeError:
            return None

    @property
    def notes(self):
        return self._notes

    def start_session(self):
        now = datetime.datetime.now()
        self._session_start = now
        self.add_note('session start', '', now)

    def elapsed_seconds_and_percentage(self):
        elapsed_seconds = (datetime.datetime.now() - self._session_start).total_seconds()
        elapsed_percentage = None if self.duration is None else elapsed_seconds / (self.duration * 60)

        return elapsed_seconds, elapsed_percentage

    def add_note(self, note_type, content, timestamp=None):
        timestamp = datetime.datetime.now() if timestamp is None else timestamp
        self._notes.append({'timestamp': timestamp, 'type': note_type, 'content': content})
        self._writer.writerow([timestamp.strftime('%Y-%m-%dT%H:%M:%S'), note_type, content])
        self._file.flush()  # flush immediately so notes are captured even on crash

    def all_notes_of_type(self, note_type):
        return [note for note in self._notes if note['type'] == note_type]

    def n_latest_notes(self, number):
        return self._notes[-number:]

    def take_screenshot(self):
        timestamp = datetime.datetime.now()
        with mss.mss() as sct:
            sct.shot(output='{}.png'.format(timestamp.strftime('%Y-%m-%dT%H%M%S')))

        self.add_note('capture', '', timestamp=timestamp)
