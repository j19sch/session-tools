import csv
import datetime
import os
import pathlib
from typing import Optional, Tuple, Type

import mss
from mypy.ipc import TracebackType


class Noter:
    def __init__(
        self, filename: Optional[str], tester: str, charter: str, duration: int
    ):
        self._notes: list = []
        self._filename = filename

        self._tester = tester
        self._charter = charter
        self._duration = duration

        self._session_start: Optional[datetime.datetime] = None

    def __enter__(self) -> "Noter":
        if self._filename is not None:
            file_path = os.path.join(os.getcwd(), "notes")
            pathlib.Path(file_path).mkdir(exist_ok=True)
            self._notes_dir = file_path
            self._file = open(
                os.path.join(self._notes_dir, self._filename), "w", newline=""
            )
            self._writer = csv.writer(
                self._file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
        self.add_note("tester", self._tester)
        self.add_note("charter", self._charter)
        self.add_note("duration", str(self._duration))
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._filename is not None:
            self._file.close()

    @property
    def duration(self) -> Optional[int]:
        try:
            return self._duration
        except AttributeError:
            return None

    @property
    def notes(self) -> list:
        return self._notes

    @property
    def session_notes(self) -> list:
        return [
            note
            for note in self._notes
            if note["type"]
            not in ["tester", "charter", "duration", "session start", "session end"]
        ]

    def start_session(self) -> None:
        now = datetime.datetime.now()
        self._session_start = now
        self.add_note("session start", "", now)

    def end_session(self) -> None:
        self.add_note("session end", "")

    def elapsed_seconds_and_percentage(self) -> Tuple[Optional[float], Optional[float]]:
        if self._session_start is None:
            elapsed_seconds = None
            elapsed_percentage = None
        else:
            elapsed_seconds = (
                datetime.datetime.now() - self._session_start
            ).total_seconds()
            elapsed_percentage = (
                None
                if self.duration is None
                else elapsed_seconds / (self.duration * 60)
            )
        return elapsed_seconds, elapsed_percentage

    def add_note(
        self, note_type: str, content: str, timestamp: datetime.datetime = None
    ) -> None:
        timestamp = datetime.datetime.now() if timestamp is None else timestamp
        self._notes.append(
            {"timestamp": timestamp, "type": note_type, "content": content}
        )
        if self._filename is not None:
            self._writer.writerow(
                [timestamp.strftime("%Y-%m-%dT%H:%M:%S"), note_type, content]
            )
            self._file.flush()  # flush immediately so notes are captured even on crash

    def all_notes_of_type(self, note_type: str) -> list:
        return [note for note in self._notes if note["type"] == note_type]

    def n_latest_notes(self, number: int) -> list:
        return self._notes[-number:]

    def take_screenshot(self) -> None:
        # ToDo: two screenshots during the same second results in the 2nd file overwriting the 1st
        timestamp = datetime.datetime.now()
        filename = timestamp.strftime("%Y%m%dT%H%M%S.png")
        screenshot_file = os.path.join(self._notes_dir, filename)
        with mss.mss() as sct:
            sct.shot(output=screenshot_file)

        self.add_note("capture", filename, timestamp=timestamp)
