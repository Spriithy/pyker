import sys
from server import instance as server
from proxy import instance as proxy
import curses
from curses import wrapper
import login_view
import lobby_view
import signal


def do_quit(x, y):
    if proxy.IDs_:
        proxy.quit()
    sys.exit(0)


signal.signal(signal.SIGINT, do_quit)


def do(stdsrc, action):
    if action == "lobby.join":
        server.join_lobby()
        lobby_view.run(stdsrc)


@curses.wrapper
def main(stdscr):
    (max_y, max_x) = stdscr.getmaxyx()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)
    do(stdscr, login_view.connection_Lobby(stdscr, max_y, max_x))