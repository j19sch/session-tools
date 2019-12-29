import curses
from datetime import datetime
from functools import partial
from noter import Noter

"""
curses docs:
lib docs: https://docs.python.org/3/library/curses.html
tutorial: https://steven.codes/blog/cs10/curses-tutorial/
how-to: https://docs.python.org/3.6/howto/curses.html
example: https://gist.github.com/claymcleod/b670285f334acd56ad1c
"""


def prompt_for_session_info(main_window):
    session_info_lines = 7
    session_info_cols = 40
    session_info_start_x = 9
    session_info_start_y = 3
    session_start_window = main_window.derwin(session_info_lines, session_info_cols, session_info_start_y, session_info_start_x)
    session_start_window.addstr(0, 0, "tester: ")
    session_start_window.addstr(1, 0, "charter: ")
    session_start_window.addstr(2, 0, "duration: ")
    session_start_window.addstr(4, 0, "press any key to start session")

    tester = session_start_window.getstr(0, 12).decode()
    charter = session_start_window.getstr(1, 12).decode()
    duration = int(session_start_window.getstr(2, 12).decode())
    curses.curs_set(0)
    session_start_window.getkey()

    main_window.clear()
    main_window.refresh()
    curses.curs_set(1)

    return tester, charter, duration


def update_summary_window(window, entries, note_types):
    window.clear()
    window.addstr(0, 1, "SUMMARY", curses.A_REVERSE)
    window.addstr(1, 1, f"entries: {len(entries)}")

    note_types_count = {}
    for note_type in note_types:
        note_types_count[note_type['type']] = 0

    found_note_types = set([note['type'] for note in entries])

    for note_type in found_note_types:
        note_types_count[note_type] = len([_ for _ in entries if _['type'] == note_type])

    position = 3
    for note_type in sorted(note_types_count):
        window.addstr(position, 1, f"{note_type}: {note_types_count[note_type]}")
        position += 1

    window.refresh()


def update_timer_window(window, noter):
    elapsed_seconds, elapsed_percentage = noter.elapsed_seconds_and_percentage()
    the_time = f"{elapsed_seconds / 60:.0f}/{str(noter.duration)}"
    window.addstr(0, 1, the_time, curses.A_BOLD)
    the_percentage = f"{elapsed_percentage:.1%}"
    window.addstr(0, 9, the_percentage, curses.A_BOLD)
    window.refresh()


def post_session_questions(window, config, noter):
    window.clear()
    window.refresh()

    post_session_lines = len(config['task_breakdown']) + 2
    post_session_cols = 40
    post_session_start_x = 9
    post_session_start_y = 3

    post_session_window = window.derwin(post_session_lines, post_session_cols, post_session_start_y, post_session_start_x)

    position = 0
    for item in config['task_breakdown']:
        post_session_window.addstr(position, 1, item)
        post_session_entry = post_session_window.getstr(position, 16).decode()
        noter.add_note(item, post_session_entry)
        position += 1

    post_session_window.addstr(position + 1, 1, "press any key to quit")

    curses.curs_set(0)
    post_session_window.getkey()
    curses.curs_set(1)


def curses_interface(stdscr, config=None):
    curses.echo()  # echo characters to screen

    stdscr.clear()
    stdscr.addstr(0, 1, f"Welcome to session noter!")
    stdscr.refresh()

    main_lines = 24
    main_cols = 120
    main_start_x = 0
    main_start_y = 2
    main_window = stdscr.derwin(main_lines, main_cols, main_start_y, main_start_x)

    tester, charter, duration = prompt_for_session_info(main_window)

    if config['noter']['output'] is not None:
        filename = f"{datetime.now().strftime('%Y%m%dT%H%M%S')}-{tester}.csv"
    else:
        filename = None

    with Noter(filename, tester, charter, duration) as noter:
        noter.start_session()

        left_window_lines = main_lines
        left_window_cols = 18
        left_window_start_y = 0
        left_window_start_x = 0
        left_window = main_window.derwin(left_window_lines, left_window_cols, left_window_start_y, left_window_start_x)
        left_window.box()

        timer_lines = 1
        timer_cols = left_window_cols - 2
        summary_lines = left_window_lines - timer_lines - 3
        summary_cols = left_window_cols - 2

        summary_start_y = 1
        summary_start_x = 1
        timer_start_y = 1 + summary_lines + 2 - 1
        timer_start_x = 1

        left_window.hline(summary_lines + 1, 1, 0, left_window_cols - 2)
        left_window.refresh()

        summary_window = left_window.derwin(summary_lines, summary_cols, summary_start_y, summary_start_x)
        update_summary_window(summary_window, noter.session_notes, config['note_types'])

        timer_window = left_window.derwin(timer_lines, timer_cols, timer_start_y, timer_start_x)
        update_timer_window(timer_window, noter)

        right_window_lines = main_lines
        right_window_cols = main_cols - left_window_cols
        right_window_start_y = 0
        right_window_start_x = left_window_cols
        right_window = main_window.derwin(right_window_lines, right_window_cols, right_window_start_y, right_window_start_x)
        right_window.box()
        right_window.refresh()

        notes_lines = summary_lines
        notes_cols = right_window_cols - 2
        prompt_lines = timer_lines
        notes_pad_type_padding = 10
        prompt_cols = right_window_cols - 2 - notes_pad_type_padding

        notes_start_y_abs = main_start_y + right_window_start_y + 1
        notes_start_x_abs = main_start_x + right_window_start_x + 1
        prompt_start_y = 1 + notes_lines + 2 - 1
        prompt_start_x = 1

        right_window.hline(notes_lines + 1, 1, 0, right_window_cols - 2)
        right_window.refresh()

        notes_pad = curses.newpad(1000, notes_cols)
        notes_pad.scrollok(True)
        notes_pad.idlok(True)  # scrolllok and idlok take care of scrolling

        prompt_window = right_window.derwin(prompt_lines, prompt_cols, prompt_start_y, prompt_start_x)
        prompt_window.refresh()

        while True:
            pass
            entry = prompt_window.getstr()
            update_timer_window(timer_window, noter)

            if entry == b"exit":
                noter.end_session()
                post_session_questions(right_window, config['post_session'], noter)
                break

            decoded_entry = entry.decode()
            try:
                note_type_command, note = decoded_entry.split(" ", maxsplit=1)
            except ValueError:
                note_type_command, note = "n", decoded_entry

            # ToDo: decide if to replace try/except with input validation
            try:
                note_type = next(_['type'] for _ in config['note_types'] if _['command'] == note_type_command)
            except StopIteration:
                note_type = note_type_command

            noter.add_note(note_type, note)

            notes = "\n".join(f"{note['type']:{notes_pad_type_padding - 1}} {note['content']}" for note in noter.session_notes)
            notes_pad.addstr(0, 0, notes)

            len_of_session_notes = len(noter.notes) - 3 - 1
            position = max(0, len_of_session_notes - notes_lines)
            notes_pad.refresh(position, 0, notes_start_y_abs, notes_start_x_abs, notes_start_y_abs + notes_lines - 1, notes_start_x_abs + notes_cols - 1)

            update_summary_window(summary_window, noter.session_notes, config['note_types'])
            prompt_window.clear()


def interface_wrapper(config):
    curses_interface_with_config = partial(curses_interface, config=config)
    curses.wrapper(curses_interface_with_config)

