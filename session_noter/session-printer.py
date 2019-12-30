import argparse

from session_noter.core.parser import session_reader
from session_noter.modules.markdown_printer import markdown_writer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file you want to convert to markdown")
    args = parser.parse_args()

    pre_session_entries, session_entries, post_session_entries = session_reader(
        args.file
    )

    markdown_writer(
        args.file, pre_session_entries, session_entries, post_session_entries
    )
