import csv


def session_parser(filename):
    pre_session = []
    post_session = []
    session = []
    with open(f"{filename}", newline='', mode='r') as session_file:
        csv_reader = csv.reader(session_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

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
