import curses
import curses.textpad as textpad
import signal
import sys
from UserClass import user

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))

lines = []
ip = '127.0.0.1:5000'


def fmt_message(message):
    return '%s <%s> %s' % (message['date'], message['from'],
                           message['content'])


def get_statusbar(w):
    lines_str = '%d' % len(lines)
    return '   %s%s%s ' % (lines_str, ' ' *
                           (w - 3 - len(lines_str) - len(ip) - 1), ip)


def run(stdscr):
    while True:
        stdscr.clear()
        (max_y, max_x) = stdscr.getmaxyx()

        for message in user.pull_Message():
            lines.append(fmt_message(message))

        for i in range(len(lines)):
            stdscr.addstr(i, 0, lines[i])

        stdscr.addstr(max_y - 2, 0, get_statusbar(max_x), curses.A_REVERSE)
        editwin = curses.newwin(1, max_x, max_y - 1, 0)
        box = textpad.Textbox(editwin)
        stdscr.refresh()
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue
        user.push_Message(text)

    stdscr.getkey()
