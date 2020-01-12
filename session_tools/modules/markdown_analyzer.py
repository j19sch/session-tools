from datetime import datetime
from statistics import median, mean

from session_tools.writers.markdown_writer import MarkDownWriter


def markdown_analyzer(sessions):
    report_types = set()
    for note_types in [session["to_report"] for session in sessions]:
        for note_type in note_types:
            report_types.add(note_type)
    report_types = list(sorted(report_types))

    report_notes = {}
    for report_type in report_types:
        report_notes[report_type] = list()
    for session in sessions:
        for note in session["session"]:
            if note[1] in report_types:
                report_notes[note[1]].append((session["filename"], note[2]))

    task_breakdown_types = set()
    for task_types in [session["task_breakdown"] for session in sessions]:
        for task_type in task_types:
            task_breakdown_types.add(task_type)
    task_breakdown_types = list(sorted(task_breakdown_types))

    with MarkDownWriter(
        f"analysis-{datetime.now().strftime('%Y%m%dT%H%M%S')}.md"
    ) as md_writer:
        col_width_default = 32
        col_width_wide = 52
        col_width_narrow = 16

        md_writer.header_1("Session analysis")

        # Overview
        md_writer.header_2("Overview")

        # Overview - time spent, number of bugs, issues, questions
        overview_1_columns = [
            ("", col_width_narrow, "L"),
            ("sessions", col_width_narrow, "C"),
            ("planned (min)", col_width_narrow, "C"),
            ("spent (min)", col_width_narrow, "C"),
        ]
        for category in report_types:
            overview_1_columns.append((category, col_width_narrow, "C"))

        overview_1_data = [
            [
                "totals",
                len(sessions),
                sum([int(session["metadata"]["duration"]) for session in sessions]),
                sum(
                    [
                        int(session["metadata"]["actual_duration"])
                        for session in sessions
                    ]
                ),
            ]
        ]

        for notes in report_notes.values():
            overview_1_data[0].append(len(notes))

        md_writer.table(overview_1_columns, overview_1_data)

        # Overview - charters
        overview_2_columns = [
            ("File", col_width_default, "L"),
            ("Tester", col_width_narrow, "L"),
            ("Charter", col_width_wide, "L"),
        ]
        overview_2_data = [
            (
                session["filename"],
                session["metadata"]["tester"],
                session["metadata"]["charter"],
            )
            for session in sessions
        ]
        md_writer.table(overview_2_columns, overview_2_data)

        # The numbers on how time spent, task breakdown
        md_writer.header_2("The numbers")

        numbers_columns = [
            ("File", col_width_default, "L"),
            ("planned (min)", col_width_narrow, "C"),
            ("spent (min)", col_width_narrow, "C"),
        ]
        for category in task_breakdown_types:
            numbers_columns.append((f"{category} (%)", col_width_narrow, "C"))

        numbers_data = []

        for session in sessions:
            session_data = [
                session["filename"],
                session["metadata"]["duration"],
                session["metadata"]["actual_duration"],
            ]

            for category in task_breakdown_types:
                session_data.append(session["task_breakdown"][category])

            numbers_data.append(session_data)

        separator = (
            " -   -   -",
            " -   -   -",
            " -   -   -",
            " -   -   -",
            " -   -   -",
            " -   -   -",
        )
        # ToDo: construct separator based on len(number_of_columns)
        numbers_data.append(separator)

        means = [
            "mean",
            round(mean([int(session["metadata"]["duration"]) for session in sessions])),
            round(
                mean(
                    [
                        int(session["metadata"]["actual_duration"])
                        for session in sessions
                    ]
                )
            ),
        ]
        for category in task_breakdown_types:
            result = round(
                mean([int(session["task_breakdown"][category]) for session in sessions])
            )
            means.append(result)
        numbers_data.append(means)

        medians = [
            "median",
            round(
                median([int(session["metadata"]["duration"]) for session in sessions])
            ),
            round(
                median(
                    [
                        int(session["metadata"]["actual_duration"])
                        for session in sessions
                    ]
                )
            ),
        ]
        for category in task_breakdown_types:
            result = round(
                median(
                    [int(session["task_breakdown"][category]) for session in sessions]
                )
            )
            medians.append(result)
        numbers_data.append(medians)

        md_writer.table(numbers_columns, numbers_data)

        for note_type, notes in report_notes.items():
            md_writer.header_2(f"{note_type.capitalize()}s")
            if len(notes) > 0:
                columns = [
                    ("File", col_width_default, "L"),
                    (note_type, col_width_wide, "L"),
                ]
                md_writer.table(columns, notes)
            else:
                md_writer.add_line(f"No {note_type}s.")
