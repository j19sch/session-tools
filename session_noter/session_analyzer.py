import argparse

from session_noter.core.utils import read_config_file
from session_noter.modules.markdown_analyzer import markdown_analyzer
from session_noter.core.read_csv_file import read_and_parse_csv_notes_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",  # ToDo: type=file, # argparse.FileType('r'),
        help="the files you want to summarize into a report",
    )
    args = parser.parse_args()

    config = read_config_file()

    sessions = [read_and_parse_csv_notes_file(file, config) for file in args.files]

    markdown_analyzer(sessions)

    print("Done!")
