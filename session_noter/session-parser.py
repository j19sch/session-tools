import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("file", help="the file you want to convert to markdown")
args = parser.parse_args()

pre_session = []
post_session = []
session = []


with open(f"{args.file}", newline='', mode='r') as session_file:
    csv_reader = csv.reader(session_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    reader_state = "pre-session"

    for row in csv_reader:
        if reader_state == "pre-session":
            if row[1] != "session start":
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


with open(f"{args.file[:-4]}.md", mode='w') as md_file:
    md_file.write("# session notes\n")

    for row in pre_session:
        md_file.write(f"**{row[1]}**: {row[2]}  \n")
    md_file.write("---\n")

    for row in post_session:
        md_file.write(f"**{row[1]}**: {row[2]}  \n")
    md_file.write("---\n")

    column_width = 19
    md_file.write(f"| {'Timestamp':{column_width}} | {'Note Type':{column_width}} | Note |\n")
    md_file.write(f"| {'':-^{column_width}} | {'':-^{column_width}} | ---- |\n")
    for row in session:
        md_file.write(f"| {row[0]:{column_width}} | {row[1]:{column_width}} | {row[2]} |\n")
