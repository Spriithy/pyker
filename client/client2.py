import sys
from server import instance as server
from proxy import instance as proxy
import curses
from curses import wrapper
import login_view
import lobby_view
import ttt_view
import signal


def do_quit(x, y):
    if proxy.username:
        proxy.quit()
    sys.exit(0)


signal.signal(signal.SIGINT, do_quit)


def do(stdscr, action):
    if action == 'lobby.join':
        server.join_lobby()
        lobby_view.run(stdscr)


@curses.wrapper
def main(stdscr):
    ttt_view.run(stdscr)
