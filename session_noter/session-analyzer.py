import argparse
from datetime import datetime
from statistics import median, mean

from markdown_writer import MarkDownWriter
from parser import session_parser


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        nargs="*",  # ToDo: type=file, # argparse.FileType('r'),
        help="the files you want to summarize into a report",
    )
    args = parser.parse_args()

    session_overview, session_numbers, bugs, issues, questions = session_parser(
        args.files
    )

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
            ("bugs", col_width_narrow, "C"),
            ("issues", col_width_narrow, "C"),
            ("questions", col_width_narrow, "C"),
        ]
        overview_1_data = [
            (
                "totals",
                len(session_overview),
                sum([int(_["duration"]) for _ in session_numbers]),
                sum([int(_["actual_duration"]) for _ in session_numbers]),
                len(bugs),
                len(issues),
                len(questions),
            )
        ]
        md_writer.table(overview_1_columns, overview_1_data)

        # Overview - charters
        overview_2_columns = [
            ("File", col_width_default, "L"),
            ("Tester", col_width_narrow, "L"),
            ("Charter", col_width_wide, "L"),
        ]
        overview_2_data = [
            (session["session_notes"], session["tester"], session["charter"])
            for session in session_overview
        ]
        md_writer.table(overview_2_columns, overview_2_data)

        # The numbers on how time spent, task breakdown
        md_writer.header_2("The numbers")

        numbers_columns = [
            ("File", col_width_default, "L"),
            ("planned (min)", col_width_narrow, "C"),
            ("spent (min)", col_width_narrow, "C"),
            ("setup (%)", col_width_narrow, "C"),
            ("testing (%)", col_width_narrow, "C"),
            ("investigating (%)", col_width_narrow, "C"),
        ]
        numbers_data = [
            (
                session["session_notes"],
                session["duration"],
                session["actual_duration"],
                session["setup"],
                session["testing"],
                session["investigating"],
            )
            for session in session_numbers
        ]

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

        means = (
            "mean",
            round(mean([int(_["duration"]) for _ in session_numbers])),
            round(mean([int(_["actual_duration"]) for _ in session_numbers])),
            round(mean([int(_["setup"]) for _ in session_numbers])),
            round(mean([int(_["testing"]) for _ in session_numbers])),
            round(mean([int(_["investigating"]) for _ in session_numbers])),
        )
        numbers_data.append(means)

        medians = (
            "median",
            round(median([int(_["duration"]) for _ in session_numbers])),
            round(median([int(_["actual_duration"]) for _ in session_numbers])),
            round(median([int(_["setup"]) for _ in session_numbers])),
            round(median([int(_["testing"]) for _ in session_numbers])),
            round(median([int(_["investigating"]) for _ in session_numbers])),
        )
        numbers_data.append(medians)
        md_writer.table(numbers_columns, numbers_data)

        # List of bugs
        md_writer.header_2("Bugs")
        if len(bugs) > 0:
            bugs_columns = [
                ("File", col_width_default, "L"),
                ("Bug", col_width_wide, "L"),
            ]
            bugs_data = [(bug["session_notes"], bug["bug"]) for bug in bugs]
            md_writer.table(bugs_columns, bugs_data)
        else:
            md_writer.add_line("No bugs.")

        # List of issues
        md_writer.header_2("Issues")
        if len(issues) > 0:
            issues_columns = [
                ("File", col_width_default, "L"),
                ("Issue", col_width_wide, "L"),
            ]
            issues_data = [(issue["session_notes"], issue["issue"]) for issue in issues]
            md_writer.table(issues_columns, issues_data)
        else:
            md_writer.add_line("No issues.")

        # List of questions
        md_writer.header_2("Questions")
        if len(questions) > 0:
            questions_columns = [
                ("File", col_width_default, "L"),
                ("Question", col_width_wide, "L"),
            ]
            questions_data = [
                (question["session_notes"], question["question"])
                for question in questions
            ]
            md_writer.table(questions_columns, questions_data)
        else:
            md_writer.add_line("No questions.")
