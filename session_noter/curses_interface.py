import curses  # https://docs.python.org/3/howto/curses.html
from copy import copy
from datetime import datetime

# example: https://gist.github.com/claymcleod/b670285f334acd56ad1c
# lib docs: https://docs.python.org/3/library/curses.html
# tutorial: https://steven.codes/blog/cs10/curses-tutorial/
# how-to: https://docs.python.org/3.6/howto/curses.html

# curses.newwin(nlines, ncols, begin_y, begin_x)
# curses.textpad.rectangle(win, uly, ulx, lry, lrx)
# window.derwin(begin_y, begin_x) // window.derwin(nlines, ncols, begin_y, begin_x)
# window.addstr(y, x, str[, attr])
from functools import partial

from noter import Noter


def update_summary_window(window, entries, note_types):
    window.clear()
    window.addstr(0, 0, "SUMMARY", curses.A_REVERSE)
    window.addstr(1, 0, f"Entries: {len(entries)}")

    note_types_count = {}
    for note_type in note_types:
        note_types_count[note_type['type']] = 0

    found_note_types = set([note['type'] for note in entries])

    for note_type in found_note_types:
        note_types_count[note_type] = len([_ for _ in entries if _['type'] == note_type])

    position = 3
    for note_type in sorted(note_types_count):
        window.addstr(position, 0, f"{note_type}: {note_types_count[note_type]}")
        position += 1

    window.refresh()


def curses_interface(stdscr, config=None):
    curses.echo()  # echo characters to screen

    stdscr.clear()

    # max y 61, max x 238
    stdscr.addstr(0, 1, f"Welcome to session noter! max dimensions: {stdscr.getmaxyx()}", curses.A_REVERSE)
    stdscr.refresh()

    session_start_window = stdscr.derwin(7, 40, 3, 3)
    session_start_window.addstr(1, 2, "tester: ")
    session_start_window.addstr(2, 2, "charter: ")
    session_start_window.addstr(3, 2, "duration: ")
    session_start_window.addstr(5, 2, "press any key to start session")

    tester = session_start_window.getstr(1, 16)
    charter = session_start_window.getstr(2, 16)
    duration = session_start_window.getstr(3, 16)
    curses.curs_set(0)
    session_start_window.getkey()

    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(1)

    filename = f"{datetime.now().strftime('%Y%m%dT%H%M%S')}-{tester}.csv"
    with Noter(None, tester, charter, duration) as noter:

        summary_lns = 15
        summary_cols = 15
        prompt_lns = 1
        prompt_cols = copy(summary_cols)
        left_pane_lns = summary_lns + prompt_lns + 3
        left_pane_cols = summary_cols + 2

        left_pane = curses.newwin(left_pane_lns, left_pane_cols, 2, 0)
        left_pane.box()
        left_pane.hline(summary_lns + 1, 1, 0, left_pane_cols - 2)
        left_pane.refresh()

        win_summary = left_pane.derwin(summary_lns, summary_cols, 1, 1)
        update_summary_window(win_summary, noter.session_notes, config['note_types'])

        win_prompt = left_pane.derwin(prompt_lns, prompt_cols, summary_lns + 2, 1)
        win_prompt.addstr(0, 1, "1234567890123", curses.A_BOLD)
        win_prompt.refresh()

        display_lns = copy(summary_lns)
        display_cols = 80
        enter_lns = 1
        enter_cols = copy(display_cols)
        right_pane_lns = display_lns + enter_lns + 3
        right_pane_cols = display_cols + 2

        right_pane = curses.newwin(right_pane_lns, right_pane_cols, 2, left_pane_cols + 1)
        right_pane.box()
        right_pane.hline(display_lns + 1, 1, 0, right_pane_cols - 2)
        right_pane.refresh()

        win_display = curses.newpad(500, 80)
        win_display.scrollok(True)
        win_display.idlok(True)  # scrolllok and idlok take care of scrolling

        win_enter = right_pane.derwin(enter_lns, enter_cols, display_lns + 2, 1)

        while True:
            entry = win_enter.getstr()  # better than Textbox
            if entry == b"exit":
                break

            decoded_entry = entry.decode()
            note_type_command, note = decoded_entry.split(" ", maxsplit=1)

            # ToDo: decide if to replace try/except with input validation
            try:
                note_type = next(_['type'] for _ in config['note_types'] if _['command'] == note_type_command)
            except StopIteration:
                note_type = note_type_command

            noter.add_note(note_type, note)

            notes = "\n".join(note['content'] for note in noter.session_notes)

            win_display.addstr(3, 0, notes)
            position = 3 + max(0, len(noter.notes) - 15)
            win_display.refresh(position, 0, 3, 19, 2+15, 18 + 80)
            update_summary_window(win_summary, noter.session_notes, config['note_types'])
            win_enter.clear()


def interface_wrapper(config):
    curses_interface_with_config = partial(curses_interface, config=config)
    curses.wrapper(curses_interface_with_config)
