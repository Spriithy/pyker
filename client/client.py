import sys
from UserClass import user as user
from ApiCalls import instance_Server as api
import curses
from curses import wrapper
import login_view
import lobby_view
import signal

signal.signal(
    signal.SIGINT, lambda x, y: ((user.quit()
                                  if user.IDs_ else True) and sys.exit(0)))


def do(stdsrc, action):
    if action == "lobby.join":
        api.join_lobby()
        lobby_view.run(stdsrc)


@curses.wrapper
def main(stdscr):
    (max_y, max_x) = stdscr.getmaxyx()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)
    do(stdscr, login_view.connection_Lobby(stdscr, max_y, max_x))