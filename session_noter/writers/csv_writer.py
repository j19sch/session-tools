import csv
from pathlib import Path
from typing import Optional, Type, Union, TextIO

from mypy.ipc import TracebackType


class CSVWriter:
    def __init__(self, path_to_file: Union[str, Path]) -> None:
        self.path_to_file = path_to_file
        self.csv_file: TextIO
        self.writer: csv._writer  # type: ignore

    def __enter__(self) -> "CSVWriter":
        self.csv_file = open(self.path_to_file, "w")
        self.writer = csv.writer(
            self.csv_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.csv_file.close()

    def add_entry(self, entry: dict) -> None:
        self.writer.writerow(
            [
                entry["timestamp"].strftime("%Y-%m-%dT%H:%M:%S"),
                entry["type"],
                entry["content"],
            ]
        )
        self.csv_file.flush()  # flush immediately so notes are captured even on crash
