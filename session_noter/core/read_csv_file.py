import csv
from datetime import datetime
from typing import Tuple


def read_and_parse_csv_notes_file(filename: str, config: dict) -> dict:
    pre_session, session_times, session, post_session = read_csv_notes_file(filename)
    metadata, session, to_report, task_breakdown = parse_csv_notes_sections(
        config, pre_session, session_times, session, post_session
    )
    session_data = {
        "filename": filename,
        "metadata": metadata,
        "session": session,
        "to_report": to_report,
        "task_breakdown": task_breakdown,
    }
    return session_data


def read_csv_notes_file(filename: str) -> Tuple[list, tuple, list, list]:
    pre_session = []
    post_session = []
    session = []
    with open(filename, newline="", mode="r") as session_file:
        csv_reader = csv.reader(
            session_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        reader_state = "pre-session"
        session_start = None
        session_end = None

        for row in csv_reader:
            if reader_state == "pre-session":
                if not row[1] == "session start":
                    pre_session.append(row)
                else:
                    session_start = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S")
                    reader_state = "session"
            elif reader_state == "session":
                if not row[1] == "session end":
                    session.append(row)
                else:
                    session_end = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S")
                    reader_state = "post-session"
            elif reader_state == "post-session":
                post_session.append(row)

    return pre_session, (session_start, session_end), session, post_session


def parse_csv_notes_sections(
    config: dict,
    pre_session: list,
    session_times: tuple,
    session: list,
    post_session: list,
) -> Tuple[dict, list, list, dict]:
    metadata = {item[1]: item[2] for item in pre_session}

    metadata["start"] = session_times[0]
    metadata["end"] = session_times[1]
    if metadata["start"] is not None and metadata["end"] is not None:
        metadata["actual_duration"] = round(
            (metadata["end"] - metadata["start"]).seconds / 60
        )
    else:
        metadata["actual_duration"] = 0

    to_report = sorted(
        [item["type"] for item in config["note_types"] if item["report"] is True]
    )

    task_breakdown = {
        item[1]: item[2]
        for item in post_session
        if item[1] in config["post_session"]["task_breakdown"]
    }

    return metadata, session, to_report, task_breakdown
