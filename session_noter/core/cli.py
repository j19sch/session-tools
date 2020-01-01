import cmd
import datetime
import math
import sys
from typing import Tuple, Optional

from session_noter.core.noter import Noter


class CLI(cmd.Cmd):
    def __init__(self, config: dict):
        print("Welcome to session-noter!\n")

        for _ in config["note_types"]:
            CLI._add_note_types_to_interface(_["type"], _["command"])
        super().__init__()

        tester, charter, duration = self._ask_for_session_info()

        filename: Optional[str]
        if config["noter"]["output"] is not None:
            filename = (
                f"{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}-{tester}.csv"
            )
        else:
            filename = None

        with Noter(filename, tester, charter, duration) as noter:
            self._noter = noter

            ready_to_go = input("Press Enter to start your session.\n")
            if ready_to_go != "":
                sys.exit()
            self._noter.start_session()

            self.prompt = self.create_prompt()
            self.cmdloop(intro="Type help or ? to list commands.")

            self._post_session(config["post_session"])

    @classmethod
    def _add_note_types_to_interface(cls, note_type: str, abbreviation: str) -> None:
        def inner_add_note_type(self: CLI, arg: str) -> None:
            self._noter.add_note(note_type, arg)

        inner_add_note_type.__doc__ = f"add a note of type {note_type}"
        inner_add_note_type.__name__ = f"do_{abbreviation}"
        setattr(cls, inner_add_note_type.__name__, inner_add_note_type)

    @staticmethod
    def _ask_for_session_info() -> Tuple[str, str, int]:
        tester = input("tester: ")
        charter = input("charter: ")
        duration: int = 0

        while True:
            try:
                duration = int(input("duration (minutes): "))
            except ValueError:
                print("Please provide a number greater than 0.")
                continue

            if duration <= 0:
                print("Please provide a number greater than 0.")
                continue
            else:
                break
        return tester, charter, duration

    def postcmd(self, stop, line):  # type: ignore
        self.prompt = self.create_prompt()
        return stop

    def create_prompt(self) -> str:
        (
            elapsed_seconds,
            elapsed_percentage,
        ) = self._noter.elapsed_seconds_and_percentage()

        if elapsed_seconds is not None:
            elapsed_minutes: int = math.floor(elapsed_seconds / 60)
            if elapsed_percentage is not None:
                prompt = f"(ntr {elapsed_minutes:.0f}/{self._noter.duration:d} {elapsed_percentage:.1%})"
            else:
                prompt = f"(ntr {elapsed_minutes:.0f}) "
        else:
            prompt = "(ntr) "

        return prompt

    def emptyline(self) -> None:  # type: ignore
        pass  # otherwise last nonempty command entered is repeated

    def _post_session(self, config: dict) -> None:
        for item in config["task_breakdown"]:
            post_session_entry = input(f"{item}: ")
            self._noter.add_note(item, post_session_entry)

    def do_list(self, arg: str) -> None:
        """list all notes so far, latest n notes, or all notes of a specific type"""
        if arg != "":
            try:
                notes = self._noter.n_latest_notes(int(arg))
            except ValueError:
                notes = self._noter.all_notes_of_type(arg)
        else:
            notes = self._noter.notes

        for note in notes:
            print(
                "{} - {:18s} {}".format(
                    note["timestamp"].strftime("%Y-%m-%dT%H:%M:%S"),
                    note["type"],
                    note["content"],
                )
            )

    def do_capt(self, _arg: None) -> None:
        """take screenshot"""
        self._noter.take_screenshot()

    def do_exit(self, _arg: None) -> bool:
        """exit"""
        self._noter.end_session()
        return True
