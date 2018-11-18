import curses  # https://docs.python.org/3/howto/curses.html
from curses.textpad import Textbox, rectangle

# example: https://gist.github.com/claymcleod/b670285f334acd56ad1c
# lib docs: https://docs.python.org/3/library/curses.html
# tutorial: https://steven.codes/blog/cs10/curses-tutorial/

# curses.newwin(nlines, ncols, begin_y, begin_x)
# curses.textpad.rectangle(win, uly, ulx, lry, lrx)


def curses_interface(stdscr):
    stdscr.clear()

    stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
    stdscr.refresh()

    # new window
    win = curses.newwin(1, 40, 3, 3)
    win.addstr(0, 0, "Top-right of sub-window", curses.A_BOLD)

    win.refresh()

    editwin = curses.newwin(5, 30, 10, 3)
    rectangle(stdscr, 9, 2, 9 + 5 + 1, 2 + 30 + 1)
    stdscr.refresh()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    message = box.gather()

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            break


def main():
    curses.wrapper(curses_interface)


if __name__ == '__main__':
    main()
