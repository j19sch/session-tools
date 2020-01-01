import csv


class CSVWriter:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.csv_file = None
        self.writer = None

    def __enter__(self):
        self.csv_file = open(self.path_to_file, "w")
        self.writer = csv.writer(
            self.csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.csv_file.close()

    def flush_file(self):
        self.csv_file.flush()
