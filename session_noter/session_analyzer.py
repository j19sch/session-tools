import argparse

from session_noter.modules.markdown_analyzer import markdown_analyzer
from session_noter.core.parser import session_parser
from session_noter.core.read_csv_file import read_csv_notes_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",  # ToDo: type=file, # argparse.FileType('r'),
        help="the files you want to summarize into a report",
    )
    args = parser.parse_args()

    session_overview, session_numbers, bugs, issues, questions = session_parser(
        args.files, read_csv_notes_file
    )

    markdown_analyzer(session_overview, session_numbers, bugs, issues, questions)
