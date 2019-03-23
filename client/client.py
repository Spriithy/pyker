import sys
import os
import InterfaceClass as itc
from ApiCalls import instance_Server as api
from UserClass import user as user
from Pinger import pinger as pinger
import curses
from curses import wrapper
import login_view
import signal

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))

@curses.wrapper
def main(stdscr):
    (max_y, max_x) = (curses.LINES, curses.COLS)
    login_view.connection_Lobby(stdscr,max_y,max_x)
    stdscr.getch()

"""
carte=".------..------..------..------..------.
|P.--. ||Y.--. ||K.--. ||E.--. ||R.--. |
| :/\: || (\/) || :/\: || (\/) || :(): |
| (__) || :\/: || :\/: || :\/: || ()() |
| '--'P|| '--'Y|| '--'K|| '--'E|| '--'R|
`------'`------'`------'`------'`------'"
"""