import curses  # https://docs.python.org/3/howto/curses.html
from copy import copy

# example: https://gist.github.com/claymcleod/b670285f334acd56ad1c
# lib docs: https://docs.python.org/3/library/curses.html
# tutorial: https://steven.codes/blog/cs10/curses-tutorial/
# how-to: https://docs.python.org/3.6/howto/curses.html

# curses.newwin(nlines, ncols, begin_y, begin_x)
# curses.textpad.rectangle(win, uly, ulx, lry, lrx)


def update_summary_window(window, entries):
    window.addstr(0, 0, "SUMMARY", curses.A_REVERSE)
    window.addstr(1, 0, f"Entries: {len(entries)}")
    window.refresh()


def curses_interface(stdscr):
    entries = []
    curses.echo()

    stdscr.clear()

    # max x 61, max y 238
    stdscr.addstr(0, 0, "Welcome to session noter!", curses.A_REVERSE)
    stdscr.refresh()

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
    update_summary_window(win_summary, entries)

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
    win_display.idlok(True)

    win_enter = right_pane.derwin(enter_lns, enter_cols, display_lns + 2, 1)

    while True:
        entry = win_enter.getstr()  # better than Textbox
        if entry == b"exit":
            break

        entries.append(entry.decode())
        win_display.addstr(3, 0, "\n".join(entries))
        position = 3 + max(0, len(entries) - 15)
        win_display.refresh(position,0, 3,19, 2+15, 18 + 80)
        update_summary_window(win_summary, entries)
        win_enter.clear()


def main():
    curses.wrapper(curses_interface)


if __name__ == '__main__':
    main()
