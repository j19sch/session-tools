import argparse

from session_noter.core.utils import read_config_file
from session_noter.core.read_csv_file import read_and_parse_csv_notes_file
from session_noter.modules.markdown_printer import markdown_writer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file you want to convert to markdown")
    args = parser.parse_args()

    config = read_config_file()

    metadata, session, to_report, task_breakdown = read_and_parse_csv_notes_file(
        args.file, config
    )

    markdown_writer(args.file, metadata, session, to_report, task_breakdown)
