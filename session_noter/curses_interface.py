import curses  # https://docs.python.org/3/howto/curses.html

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

    win_summary_outer = curses.newwin(15 + 2, 15 + 2, 2, 0)
    win_summary_outer.box()
    win_summary_outer.refresh()
    win_summary = win_summary_outer.derwin(15, 15, 1, 1)
    update_summary_window(win_summary, entries)

    win_prompt = curses.newwin(1 + 2, 15 + 2, 18, 0)
    win_prompt.box()
    win_prompt.addstr(1, 1, "1234567890", curses.A_BOLD)
    win_prompt.refresh()

    win_display_outer = curses.newwin(15 + 2, 80 + 2, 2, 18)
    win_display_outer.box()
    win_display_outer.refresh()
    win_display = curses.newpad(500, 80)
    win_display.scrollok(True)
    win_display.idlok(True)

    win_enter_outer = curses.newwin(1 + 2, 80 + 2, 18, 18)
    win_enter_outer.box()
    win_enter_outer.refresh()
    win_enter = win_enter_outer.derwin(1, 68, 1, 1)

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
