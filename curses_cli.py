import curses  # https://docs.python.org/3/howto/curses.html

# starting
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

stdscr.keypad(True)


stdscr.addstr(0, 0, "Current mode: Typing mode", curses.A_REVERSE)
stdscr.refresh()

# new window
begin_x = 20
begin_y = 7
height = 5
width = 40
win = curses.newwin(height, width, begin_y, begin_x)
win.addstr(0, 0, "Top-right of sub-window", curses.A_BOLD)

win.refresh()

while True:
    c = stdscr.getch()
    if c == ord('q'):
        break

# terminating
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
