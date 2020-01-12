from session_tools.writers.markdown_writer import MarkDownWriter


def markdown_writer(session_data):
    with MarkDownWriter(
        f"{session_data['filename'][:-4]}.md"  # ToDo: use PathLib's PurePath.stem
    ) as md_writer:
        md_writer.header_1("Session notes")

        # tester, charter, duration
        for k, v in session_data["metadata"].items():
            if k in ["duration", "actual_duration"]:
                md_writer.add_line(f"**{k.replace('_', ' ')}**: {v} minutes")
            else:
                md_writer.add_line(f"**{k.replace('_', ' ')}**: {v}")

        md_writer.newline()
        md_writer.separator()
        md_writer.newline()

        # task breakdown
        for k, v in session_data["task_breakdown"].items():
            md_writer.add_line(f"**{k}**: {v}%")

        md_writer.newline()
        md_writer.separator()
        md_writer.newline()

        # session log
        column_width = 19
        columns = [
            ("Timestamp", column_width, "L"),
            ("Note type", column_width, "L"),
            ("Note", column_width, "L"),
        ]
        data = [(entry[0], entry[1], entry[2]) for entry in session_data["session"]]
        md_writer.table(columns, data)

        col_width_default = 32
        col_width_wide = 52

        # note type to report
        for note_type in session_data["to_report"]:
            md_writer.header_2(note_type)
            notes = [note for note in session_data["session"] if note[1] == note_type]
            if len(notes) > 0:
                columns = [
                    ("Timestamp", col_width_default, "L"),
                    ("Entry", col_width_wide, "L"),
                ]
                data = [(entry[0], entry[2]) for entry in notes]
                md_writer.table(columns, data)
            else:
                md_writer.add_line(f"No {note_type}s.")
                md_writer.newline()
