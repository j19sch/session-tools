import argparse
from datetime import datetime
from statistics import median, mean

from parser import session_parser


def analyze_notes(notes):
    pre_session, session, post_session = session_parser(notes)

    overview = {"session_notes": notes}
    numbers = {"session_notes": notes}

    for item in pre_session:
        if item[1] in ["tester", "charter"]:
            overview[item[1]] = item[2]
        elif item[1] == "duration":
            numbers[item[1]] = item[2]

    start_time = None
    end_time = None

    for item in session:
        if item[1] == "session start":
            start_time = datetime.strptime(item[0], '%Y-%m-%dT%H:%M:%S')
        elif item[1] == "session end":
            end_time = datetime.strptime(item[0], '%Y-%m-%dT%H:%M:%S')
        elif item[1] == "bug":
            bugs.append({"bug": item[2],
                         "session_notes": notes})
        elif item[1] == "issue":
            issues.append({"issue": item[2],
                           "session_notes": notes})
        elif item[1] == "questions":
            bugs.append({"questions": item[2],
                         "session_notes": notes})

    try:
        numbers["actual_duration"] = round((end_time - start_time).seconds / 60)
    except TypeError:
        numbers["actual_duration"] = 0

    session_overview.append(overview)
    session_numbers.append(numbers)

    numbers.update({item[1]: item[2] for item in post_session})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='*',  # ToDo: type=file, # argparse.FileType('r'),
                        help="the files you want to summarize into a report")
    args = parser.parse_args()

    session_overview = []
    session_numbers = []
    bugs = []
    issues = []
    questions = []

    for file in args.files:
        analyze_notes(file)

    with open(f"analysis-{datetime.now().strftime('%Y%m%dT%H%M%S')}.md", mode='w') as md_file:
        md_file.write("# session analysis\n")

        col_width_default = 32
        col_width_wide = 52
        col_width_narrow = 16

        md_file.write("## Overview\n")

        md_file.write(f"| {'':{col_width_narrow}} | "
                      f"{'sessions':{col_width_narrow}} | "
                      f"{'planned (min)':{col_width_narrow}} | "
                      f"{'spent (min)':{col_width_narrow}} | "
                      f"{'bugs':{col_width_narrow}} | "
                      f"{'issues':{col_width_narrow}} | "
                      f"{'questions':{col_width_narrow}} |\n")
        md_file.write(f"| {'':-^{col_width_narrow}} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | " 
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} |\n")
        md_file.write(f"| {'totals':{col_width_narrow}} | "
                      f"{len(session_overview):{col_width_narrow}} | "
                      f"{sum([int(_['duration']) for _ in session_numbers]):{col_width_narrow}} | "
                      f"{sum([int(_['actual_duration']) for _ in session_numbers]):{col_width_narrow}} | "
                      f"{len(bugs):{col_width_narrow}} | "
                      f"{len(issues):{col_width_narrow}} | "
                      f"{len(questions):{col_width_narrow}} |\n")
        md_file.write("\n")

        md_file.write(f"| {'File':{col_width_default}} | "
                      f"{'Tester':{col_width_narrow}} | "
                      f"{'Charter':{col_width_wide}} |\n")
        md_file.write(f"| {'':-^{col_width_default}} | "
                      f"{'':-^{col_width_narrow}} | " 
                      f"{'':-^{col_width_wide}} |\n")
        for session in session_overview:
            md_file.write(f"| {session['session_notes']:{col_width_default}} | "
                          f"{session['tester']:{col_width_narrow}} | "
                          f"{session['charter']:{col_width_wide}} |\n")
        md_file.write("\n")

        md_file.write("## The numbers\n")
        md_file.write(f"| {'File':{col_width_default}} | "
                      f"{'Planned (min)':{col_width_narrow}} | "
                      f"{'Spent (min)':{col_width_narrow}} | "
                      f"{'Setup (%)':{col_width_narrow}} | "
                      f"{'Testing (%)':{col_width_narrow}} | "
                      f"{'Investigating (%)':{col_width_narrow}} |\n")
        md_file.write(f"| {'':-^{col_width_default}} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | " 
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} | "
                      f"{':' + '-'*(col_width_narrow-2) + ':'} |\n")
        for session in session_numbers:
            md_file.write(f"| {session['session_notes']:{col_width_default}} | "
                          f"{session['duration']:{col_width_narrow}} | "
                          f"{session['actual_duration']:{col_width_narrow}} | "
                          f"{session['setup']:{col_width_narrow}} | "
                          f"{session['testing']:{col_width_narrow}} | "
                          f"{session['investigating']:{col_width_narrow}} |\n")

        md_file.write(f"| {' -   -   -':{col_width_default}} | {'-   -   -':{col_width_narrow}} | {'-   -   -':{col_width_narrow}} "
                      f"| {'-   -   -':{col_width_narrow}} | {'-   -   -':{col_width_narrow}} | {'-   -   -':{col_width_narrow}} |\n")
        md_file.write(f"| {'mean':{col_width_default}} | "
                      f"{round(mean([int(_['duration']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(mean([int(_['actual_duration']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(mean([int(_['setup']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(mean([int(_['testing']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(mean([int(_['investigating']) for _ in session_numbers])):{col_width_narrow}} | \n")
        md_file.write(f"| {'median':{col_width_default}} | "
                      f"{round(median([int(_['duration']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(median([int(_['actual_duration']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(median([int(_['setup']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(median([int(_['testing']) for _ in session_numbers])):{col_width_narrow}} | "
                      f"{round(median([int(_['investigating']) for _ in session_numbers])):{col_width_narrow}} | \n")
        md_file.write("\n")

        md_file.write("## Bugs\n")
        if len(bugs) > 0:
            md_file.write(f"| {'File':{col_width_default}} | {'Bug':{col_width_wide}} |\n")
            md_file.write(f"| {'':-^{col_width_default}} | {'':-^{col_width_wide}} |\n")
            for bug in bugs:
                md_file.write(f"| {bug['session_notes']:{col_width_default}} | {bug['bug']:{col_width_wide}} |\n")
        else:
            md_file.write("No bugs.")
        md_file.write("\n")

        md_file.write("## Issues\n")
        if len(issues) > 0:
            md_file.write(f"| {'File':{col_width_default}} | {'Issue':{col_width_wide}} |\n")
            md_file.write(f"| {'':-^{col_width_default}} | {'':-^{col_width_wide}} |\n")
            for issue in issues:
                md_file.write(f"| {issue['session_notes']:{col_width_default}} | {issue['issue']:{col_width_wide}} |\n")
        else:
            md_file.write("No issues.")
        md_file.write("\n")

        md_file.write("## Questions\n")
        if len(questions) > 0:
            md_file.write(f"| {'File':{col_width_default}} | {'Question':{col_width_wide}} |\n")
            md_file.write(f"| {'':-^{col_width_default}} | {'':-^{col_width_wide}} |\n")
            for issue in questions:
                md_file.write(f"| {issue['session_notes']:{col_width_default}} | {issue['question']:{col_width_wide}} |\n")
        else:
            md_file.write("No questions.")
        md_file.write("\n")
