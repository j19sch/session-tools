import datetime
from unittest import mock
import pytest

from session_noter.core.noter import Noter
from session_noter.writers.csv_writer import CSVWriter


def test_add_session_info_notes_at_start():
    tester = "the tester"
    charter = "my charter"
    duration = 10

    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, tester, charter, duration)
    assert noter.notes[0]["type"] == "tester"
    assert noter.notes[0]["content"] == tester
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime

    assert noter.notes[1]["type"] == "charter"
    assert noter.notes[1]["content"] == charter
    assert type(noter.notes[1]["timestamp"]) == datetime.datetime

    assert noter.notes[2]["type"] == "duration"
    assert noter.notes[2]["content"] == str(duration)
    assert type(noter.notes[2]["timestamp"]) == datetime.datetime

    assert writer.add_entry.call_count == 3

    import logging

    logging.info(writer.add_entry.call_args_list)

    # [0][0][0]: first call, positional args (aot keyword args), first positional arg
    assert writer.add_entry.call_args_list[0][0][0]["type"] == "tester"
    assert writer.add_entry.call_args_list[0][0][0]["content"] == tester

    assert writer.add_entry.call_args_list[1][0][0]["type"] == "charter"
    assert writer.add_entry.call_args_list[1][0][0]["content"] == charter

    assert writer.add_entry.call_args_list[2][0][0]["type"] == "duration"
    assert writer.add_entry.call_args_list[2][0][0]["content"] == str(duration)


@pytest.mark.skip(reason="needs mock for CSVWriter instance")
def test_duration_property():
    noter = Noter(None, "tester", "charter", 10)
    assert noter.duration == 10


@pytest.mark.skip(reason="needs mock for CSVWriter instance")
def test_notes_property():
    tester = "the tester"
    charter = "my charter"
    duration = 10

    with Noter(None, tester, charter, duration) as noter:
        assert len(noter.notes) == 3
        noter.add_note("note", "some note")
        assert len(noter.notes) == 4


@pytest.mark.skip(reason="needs mock for CSVWriter instance")
def test_session_notes_property():
    with Noter(None, "tester", "charter", 10) as noter:
        assert len(noter.session_notes) == 0
        noter.add_note("note", "some note")
        assert len(noter.session_notes) == 1


@pytest.mark.skip(reason="needs mock for CSVWriter instance")
def test_start_session():
    noter = Noter(None, "tester", "charter", 10)
    noter.start_session()

    assert len(noter.notes) == 1
    assert noter.notes[0]["type"] == "session start"
    assert noter.notes[0]["content"] == ""
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime


@pytest.mark.skip(reason="needs mock for CSVWriter instance")
def test_end_session():
    noter = Noter(None, "tester", "charter", 10)
    noter.end_session()

    assert len(noter.notes) == 1
    assert noter.notes[0]["type"] == "session end"
    assert noter.notes[0]["content"] == ""
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime


@pytest.mark.skip(reason="needs mock for CSVWriter instance")
def test_add_note():
    noter = Noter(None, "tester", "charter", 10)
    noter.add_note("note", "test content")

    assert len(noter.notes) == 1
    assert noter.notes[0]["type"] == "note"
    assert noter.notes[0]["content"] == "test content"
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime
