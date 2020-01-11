from session_noter.writers.markdown_writer import MarkDownWriter


def markdown_writer(filename, metadata, session, to_report, task_breakdown):
    with MarkDownWriter(
        f"{filename[:-4]}.md"  # ToDo: use PathLib's PurePath.stem
    ) as md_writer:
        md_writer.header_1("Session notes")

        # tester, charter, duration
        for k, v in metadata.items():
            if k in ["duration", "actual_duration"]:
                md_writer.add_line(f"**{k.replace('_', ' ')}**: {v} minutes")
            else:
                md_writer.add_line(f"**{k.replace('_', ' ')}**: {v}")

        md_writer.newline()
        md_writer.separator()
        md_writer.newline()

        # task breakdown
        for k, v in task_breakdown.items():
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
        data = [(entry[0], entry[1], entry[2]) for entry in session]
        md_writer.table(columns, data)

        col_width_default = 32
        col_width_wide = 52

        # reportable entries
        for k, v in to_report.items():
            md_writer.header_2(k)
            if len(v) > 0:
                columns = [
                    ("Timestamp", col_width_default, "L"),
                    ("Entry", col_width_wide, "L"),
                ]
                data = [(entry[0], entry[2]) for entry in v]
                md_writer.table(columns, data)
            else:
                md_writer.add_line(f"No {k}s.")
                md_writer.newline()
