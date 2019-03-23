import curses
import signal
import sys

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))


def read_str(stdscr, y, x, n, prompt=''):
    curses.echo()
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    input = stdscr.getstr(y, len(prompt) + 1 + x, n)
    return input


@curses.wrapper
def main(stdscr):
    # Clear screen
    stdscr.clear()

    (max_y, max_x) = (curses.LINES, curses.COLS)
    text = 'Type in your username'
    stdscr.addstr(max_y // 3, max_x // 2 - len(text) // 2, text, curses.A_BOLD)
    user_name = read_str(stdscr, max_y // 3 + 1,
                         max_x // 2 - len(text) // 2 - 2, len(text), '$')

    connect(user_name)

    stdscr.refresh()
    stdscr.getkey()
