from session_tools.writers import csv_writer
from unittest import mock
from datetime import datetime


def test_csv_writer():
    entry = {"timestamp": datetime.now(), "type": "note", "content": "just a note"}
    path_to_file = "/tmp/test-file.csv"

    with mock.patch("builtins.open", new_callable=mock.mock_open()) as m:
        with csv_writer.CSVWriter(path_to_file) as writer:
            m.assert_called_once_with(path_to_file, "w")

            writer.add_entry(entry)
            file_handle = m()
            file_handle.write.assert_called_once_with(
                f'{entry["timestamp"].strftime("%Y-%m-%dT%H:%M:%S")};{entry["type"]};{entry["content"]}\r\n'
            )
            file_handle.flush.assert_called_once()

        file_handle.close.assert_called_once()
