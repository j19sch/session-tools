import argparse

from parser import session_reader
from markdown_writer import MarkDownWriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file you want to convert to markdown")
    args = parser.parse_args()

    pre_session_entries, session_entries, post_session_entries = session_reader(
        args.file
    )

    with MarkDownWriter(f"{args.file[:-4]}-new.md") as md_writer:
        md_writer.header_1("Session notes")

        # tester, charter, duration
        for entry in pre_session_entries:
            if entry[1] == "duration":
                md_writer.add_line(f"**{entry[1]}**: {entry[2]} minutes")
            else:
                md_writer.add_line(f"**{entry[1]}**: {entry[2]}")

        md_writer.separator()

        # task breakdown
        for entry in post_session_entries:
            md_writer.add_line(f"**{entry[1]}**: {entry[2]}%")

        md_writer.separator()

        # session log
        column_width = 19
        columns = [
            ("Timestamp", column_width, "L"),
            ("Note type", column_width, "L"),
            ("Note", column_width, "L"),
        ]
        data = [(entry[0], entry[1], entry[2]) for entry in session_entries]
        md_writer.table(columns, data)
