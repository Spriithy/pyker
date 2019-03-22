import sys
import os
import InterfaceClass as itc
from ApiCalls import instance_Server as api
from UserClass import user as user
from Pinger import pinger as pinger
import curses
from curses import wrapper


def main(stdscr):
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(1, 9):
        v = i - 10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10 / v))

    stdscr.refresh()
    stdscr.getkey()


wrapper(main)
