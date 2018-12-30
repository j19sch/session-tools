import csv


class WriterCSV:
    def __enter__(self):
        self._file = open('noter.csv', 'w', newline='')
        self._writer = csv.writer(self._file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        return self

    def write_note(self, timestamp, note_type, content):
        self._writer.writerow([timestamp.strftime('%Y-%m-%dT%H:%M:%S'), note_type, content])
        self._file.flush()  # flush immediately so notes are captured even on crash

    def __exit__(self, exc_type, exc_val, exc_traceback):
        self._file.close()
