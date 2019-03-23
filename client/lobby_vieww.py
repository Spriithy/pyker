import curses
import signal
import sys

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))


def read_str(stdscr, y, x, n, prompt=''):
    curses.echo()
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    text = stdscr.getstr(y, len(prompt) + 1 + x, n)
    curses.noecho()
    return str(text, 'utf-8')


lines = []


def get_statusbar(w):
    lines_str = '%d' % len(lines)
    return '   %s%s' % (lines_str, ' ' * (w - 3 - len(lines_str)))


def run(stdscr):
    (max_y, max_x) = stdscr.getmaxyx()
    while True:
        stdscr.clear()
        for i in range(len(lines)):
            stdscr.addstr(i, 0, '<Spriithy> ' + lines[i])

        stdscr.addstr(max_y - 2, 0, get_statusbar(max_x), curses.A_REVERSE)

        message = read_str(stdscr, max_y - 1, 0, max_x, '>')
        lines.append(message)

        stdscr.refresh()

    stdscr.getkey()
