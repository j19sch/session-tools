import argparse

from session_noter.core.utils import read_config_file
from session_noter.core.read_csv_file import read_and_parse_csv_notes_file
from session_noter.modules.markdown_printer import markdown_writer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file you want to convert to markdown")
    args = parser.parse_args()

    config = read_config_file()

    session_data = read_and_parse_csv_notes_file(args.file, config)

    markdown_writer(session_data)
    print("Done!")
