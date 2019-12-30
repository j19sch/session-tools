import csv
from datetime import datetime


def session_parser(files: list):
    session_overview = []
    session_numbers = []
    bugs = []
    issues = []
    questions = []

    for file in files:
        pre_session, session, post_session = session_reader(file)

        overview = {"session_notes": file}
        numbers = {"session_notes": file}

        for item in pre_session:
            if item[1] in ["tester", "charter"]:
                overview[item[1]] = item[2]
            elif item[1] == "duration":
                numbers[item[1]] = item[2]

        start_time = None
        end_time = None

        for item in session:
            if item[1] == "session start":
                start_time = datetime.strptime(item[0], "%Y-%m-%dT%H:%M:%S")
            elif item[1] == "session end":
                end_time = datetime.strptime(item[0], "%Y-%m-%dT%H:%M:%S")
            elif item[1] == "bug":
                bugs.append({"bug": item[2], "session_notes": file})
            elif item[1] == "issue":
                issues.append({"issue": item[2], "session_notes": file})
            elif item[1] == "question":
                questions.append({"question": item[2], "session_notes": file})

        try:
            numbers["actual_duration"] = round((end_time - start_time).seconds / 60)
        except TypeError:
            numbers["actual_duration"] = 0

        session_overview.append(overview)
        session_numbers.append(numbers)

        numbers.update({item[1]: item[2] for item in post_session})

    return session_overview, session_numbers, bugs, issues, questions


def session_reader(filename):
    pre_session = []
    post_session = []
    session = []
    with open(filename, newline="", mode="r") as session_file:
        csv_reader = csv.reader(
            session_file, delimiter=";", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        reader_state = "pre-session"

        for row in csv_reader:
            if reader_state == "pre-session":
                if not row[1] == "session start":
                    pre_session.append(row)
                else:
                    reader_state = "session"
                    session.append(row)
            elif reader_state == "session":
                session.append(row)
                if row[1] == "session end":
                    reader_state = "post-session"
            elif reader_state == "post-session":
                post_session.append(row)

    return pre_session, session, post_session
