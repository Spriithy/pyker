import sys
from UserClass import user as user
import curses
from curses import wrapper
import login_view
import lobby_view
import signal

signal.signal(signal.SIGINT, lambda x, y: (user.quit() and sys.exit(0)))


def do(stdsrc, action):
    if action == "lobby.join":
        lobby_view.run(stdsrc)


@curses.wrapper
def main(stdscr):
    (max_y, max_x) = stdscr.getmaxyx()
    do(stdscr, login_view.connection_Lobby(stdscr, max_y, max_x))