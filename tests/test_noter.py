import datetime

from session_noter.core.noter import Noter


def test_add_session_info_notes_at_start():
    tester = "the tester"
    charter = "my charter"
    duration = 10

    with Noter(None, tester, charter, duration) as noter:
        assert noter.notes[0]["type"] == "tester"
        assert noter.notes[0]["content"] == tester
        assert type(noter.notes[0]["timestamp"]) == datetime.datetime

        assert noter.notes[1]["type"] == "charter"
        assert noter.notes[1]["content"] == charter
        assert type(noter.notes[1]["timestamp"]) == datetime.datetime

        assert noter.notes[2]["type"] == "duration"
        assert noter.notes[2]["content"] == str(duration)
        assert type(noter.notes[2]["timestamp"]) == datetime.datetime


def test_duration_property():
    noter = Noter(None, "tester", "charter", 10)
    assert noter.duration == 10


def test_notes_property():
    tester = "the tester"
    charter = "my charter"
    duration = 10

    with Noter(None, tester, charter, duration) as noter:
        assert len(noter.notes) == 3
        noter.add_note("note", "some note")
        assert len(noter.notes) == 4


def test_session_notes_property():
    with Noter(None, "tester", "charter", 10) as noter:
        assert len(noter.session_notes) == 0
        noter.add_note("note", "some note")
        assert len(noter.session_notes) == 1


def test_start_session():
    noter = Noter(None, "tester", "charter", 10)
    noter.start_session()

    assert len(noter.notes) == 1
    assert noter.notes[0]["type"] == "session start"
    assert noter.notes[0]["content"] == ""
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime


def test_end_session():
    noter = Noter(None, "tester", "charter", 10)
    noter.end_session()

    assert len(noter.notes) == 1
    assert noter.notes[0]["type"] == "session end"
    assert noter.notes[0]["content"] == ""
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime


def test_add_note():
    noter = Noter(None, "tester", "charter", 10)
    noter.add_note("note", "test content")

    assert len(noter.notes) == 1
    assert noter.notes[0]["type"] == "note"
    assert noter.notes[0]["content"] == "test content"
    assert type(noter.notes[0]["timestamp"]) == datetime.datetime
