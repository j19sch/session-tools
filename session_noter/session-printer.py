import argparse

from parser import session_parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file you want to convert to markdown")
    args = parser.parse_args()

    pre_session_entries, session_entries, post_session_entries = session_parser(args.file)

    with open(f"{args.file[:-4]}.md", mode='w') as md_file:
        md_file.write("# session notes\n")

        for entry in pre_session_entries:
            if entry[1] == "duration":
                md_file.write(f"**{entry[1]}**: {entry[2]} minutes  \n")
            else:
                md_file.write(f"**{entry[1]}**: {entry[2]}  \n")
        md_file.write("---\n")

        for entry in post_session_entries:
            md_file.write(f"**{entry[1]}**: {entry[2]}%  \n")
        md_file.write("---\n")

        column_width = 19
        md_file.write(f"| {'Timestamp':{column_width}} | {'Note Type':{column_width}} | Note |\n")
        md_file.write(f"| {'':-^{column_width}} | {'':-^{column_width}} | ---- |\n")
        for entry in session_entries:
            md_file.write(f"| {entry[0]:{column_width}} | {entry[1]:{column_width}} | {entry[2]} |\n")
