import datetime
import pathlib
from typing import Optional, Tuple

import mss

from session_tools.writers.csv_writer import CSVWriter


class Noter:
    # ToDo: should the Noter take a filename, a filehandler or a writer?
    def __init__(self, writer: CSVWriter, tester: str, charter: str, duration: int):
        self._writer = writer
        self._notes: list = []
        self._notes_dir = pathlib.Path(writer.path_to_file).parent.resolve()

        self._tester = tester
        self._charter = charter
        self._duration = duration

        self._session_start: Optional[datetime.datetime] = None

        self.add_note("tester", self._tester)
        self.add_note("charter", self._charter)
        self.add_note("duration", str(self._duration))

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
        note = {"timestamp": timestamp, "type": note_type, "content": content}

        self._notes.append(note)
        self._writer.add_entry(note)

    def all_notes_of_type(self, note_type: str) -> list:
        return [note for note in self._notes if note["type"] == note_type]

    def n_latest_notes(self, number: int) -> list:
        return self._notes[-number:]

    def take_screenshot(self) -> None:
        timestamp = datetime.datetime.now()
        base_filename = timestamp.strftime("%Y%m%dT%H%M%S")

        filename = f"{base_filename}.png"
        screenshot_file = self._notes_dir.joinpath(filename)

        if pathlib.Path(screenshot_file).is_file():
            suffix = 1
            while self._notes_dir.joinpath(f"{base_filename}-{suffix}.png").is_file():
                suffix += 1
            filename = f"{base_filename}-{suffix}.png"
            screenshot_file = self._notes_dir.joinpath(filename)

        with mss.mss() as sct:
            sct.shot(output=str(screenshot_file))

        self.add_note("capture", filename, timestamp=timestamp)
        print(f"captured {filename}")
