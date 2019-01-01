import argparse
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file you want to convert to markdown")
    args = parser.parse_args()

    pre_session_entries, session_entries, post_session_entries = session_parser(args.file)

    with open(f"{args.file[:-4]}.md", mode='w') as md_file:
        md_file.write("# session notes\n")

        for entry in pre_session_entries:
            md_file.write(f"**{entry[1]}**: {entry[2]}  \n")
        md_file.write("---\n")

        for entry in post_session_entries:
            md_file.write(f"**{entry[1]}**: {entry[2]}  \n")
        md_file.write("---\n")

        column_width = 19
        md_file.write(f"| {'Timestamp':{column_width}} | {'Note Type':{column_width}} | Note |\n")
        md_file.write(f"| {'':-^{column_width}} | {'':-^{column_width}} | ---- |\n")
        for entry in session_entries:
            md_file.write(f"| {entry[0]:{column_width}} | {entry[1]:{column_width}} | {entry[2]} |\n")
