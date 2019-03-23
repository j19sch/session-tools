import curses  # https://docs.python.org/3/howto/curses.html
from curses.textpad import Textbox, rectangle

# example: https://gist.github.com/claymcleod/b670285f334acd56ad1c
# lib docs: https://docs.python.org/3/library/curses.html
# tutorial: https://steven.codes/blog/cs10/curses-tutorial/
# how-to: https://docs.python.org/3.6/howto/curses.html

# curses.newwin(nlines, ncols, begin_y, begin_x)
# curses.textpad.rectangle(win, uly, ulx, lry, lrx)


def curses_interface(stdscr):
    entries = []
    curses.echo()

    stdscr.clear()

    stdscr.addstr(0, 0, "Welcome to session noter!", curses.A_REVERSE)
    stdscr.refresh()

    win_display_outer = curses.newwin(15 + 2, 80 + 2, 2, 0)
    win_display_outer.border()
    win_display_outer.refresh()
    win_display_inner = win_display_outer.derwin(15, 80, 1, 1)

    win_prompt = curses.newwin(1 + 2, 10 + 2, 18, 0)
    win_prompt.border()
    win_prompt.addstr(1, 1, "1234567890", curses.A_BOLD)
    win_prompt.refresh()

    win_enter_outer = curses.newwin(1 + 2, 68 + 2, 18, 12)
    win_enter_outer.border()
    win_enter_outer.refresh()

    win_enter_inner = win_enter_outer.derwin(1, 68, 1, 1)

    while True:
        entry = win_enter_inner.getstr()  # better than Textbox
        if entry == b"exit":
            break

        entries.append(entry.decode())
        win_display_inner.addstr(3, 0, "\n".join(entries))
        win_display_inner.refresh()
        win_enter_inner.clear()


def main():
    curses.wrapper(curses_interface)


if __name__ == '__main__':
    main()
