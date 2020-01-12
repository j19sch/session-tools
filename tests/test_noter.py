import datetime
from unittest import mock

from session_tools.core.noter import Noter
from session_tools.writers.csv_writer import CSVWriter


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


def test_duration_property():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, "tester", "charter", 10)
    assert noter.duration == 10


def test_notes_property():
    tester = "the tester"
    charter = "my charter"
    duration = 10

    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, tester, charter, duration)
    assert len(noter.notes) == 3
    noter.add_note("note", "some note")
    assert len(noter.notes) == 4


def test_session_notes_property():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, "tester", "charter", 10)
    assert len(noter.session_notes) == 0
    noter.add_note("note", "some note")
    assert len(noter.session_notes) == 1


def test_start_session():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, "tester", "charter", 10)
    noter.start_session()

    assert len(noter.notes) == 4
    assert noter.notes[3]["type"] == "session start"
    assert noter.notes[3]["content"] == ""
    assert type(noter.notes[3]["timestamp"]) == datetime.datetime


def test_end_session():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, "tester", "charter", 10)
    noter.end_session()

    assert len(noter.notes) == 4
    assert noter.notes[3]["type"] == "session end"
    assert noter.notes[3]["content"] == ""
    assert type(noter.notes[3]["timestamp"]) == datetime.datetime


def test_add_note():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")

    noter = Noter(writer, "tester", "charter", 10)
    noter.add_note("note", "test content")

    assert len(noter.notes) == 4
    assert noter.notes[3]["type"] == "note"
    assert noter.notes[3]["content"] == "test content"
    assert type(noter.notes[3]["timestamp"]) == datetime.datetime


def test_elapsed_seconds_session_start_not_set():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")
    noter = Noter(writer, "tester", "charter", 10)

    assert noter.elapsed_seconds_and_percentage() == (None, None)


def test_elapsed_seconds_session_start_and_duration_set():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")
    duration = 10
    noter = Noter(writer, "tester", "charter", duration)

    noter._session_start = datetime.datetime(2020, 1, 1, 10, 0, 0, 000000)
    with mock.patch("session_tools.core.noter.datetime") as mock_date:
        mocked_current_time = datetime.datetime(2020, 1, 1, 10, 2, 0, 000000)
        mock_date.datetime.now.return_value = mocked_current_time
        mock_date.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        expected_elapsed_seconds = (
            mocked_current_time - noter._session_start
        ).total_seconds()

        assert noter.elapsed_seconds_and_percentage() == (
            expected_elapsed_seconds,
            expected_elapsed_seconds / (duration * 60),
        )


def test_take_screenshot():
    writer = mock.Mock(spec=CSVWriter(""), path_to_file="uhugh")
    noter = Noter(writer, "tester", "charter", 10)

    with mock.patch("session_tools.core.noter.mss.mss") as mock_mss, mock.patch(
        "session_tools.core.noter.datetime"
    ) as mock_date:
        mocked_current_time = datetime.datetime(2020, 1, 1, 10, 2, 0, 000000)
        mock_date.datetime.now.return_value = mocked_current_time
        mock_date.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_sct = mock.Mock()
        mock_mss.return_value.__enter__.return_value = mock_sct

        noter.take_screenshot()

        assert mock_sct.shot.call_count == 1
        assert mock_sct.shot.call_args[1] == {
            "output": f"{noter._notes_dir}/20200101T100200.png"
        }

    assert len(noter.notes) == 4
    assert noter.notes[3]["type"] == "capture"
    assert noter.notes[3]["content"] == mocked_current_time.strftime(
        "%Y%m%dT%H%M%S.png"
    )
    assert type(noter.notes[3]["timestamp"]) == datetime.datetime
