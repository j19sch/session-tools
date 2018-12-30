import datetime
import mss


class Noter:
    def __init__(self, writer, tester, charter, duration):
        # ToDo: dynamic adding of attributes
        self._notes = []
        self._writer = writer

        self._tester = tester
        self.add_note('duration', self._tester)

        self._charter = charter
        self.add_note('duration', self._charter)

        self._duration = int(duration)
        self.add_note('duration', self._duration)

        self._session_start = None

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
        self._writer.write_note(timestamp, note_type, content)

    def all_notes_of_type(self, note_type):
        return [note for note in self._notes if note['type'] == note_type]

    def n_latest_notes(self, number):
        return self._notes[-number:]

    def take_screenshot(self):
        timestamp = datetime.datetime.now()
        with mss.mss() as sct:
            sct.shot(output='{}.png'.format(timestamp.strftime('%Y-%m-%dT%H%M%S')))

        self.add_note('capture', '', timestamp=timestamp)
