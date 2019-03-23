import curses
import signal
import sys
from ApiCalls import instance_Server as api
from UserClass import user as user

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))


def read_str(stdscr, y, x, n, prompt=''):
    curses.echo()
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    text = stdscr.getstr(y, len(prompt) + 1 + x, n)
    curses.noecho()
    return str(text,'utf-8')

def connection_Lobby(stdscr,max_y, max_x):
    stdscr.clear()
    text = 'Type in your username'
    stdscr.addstr(max_y // 3, max_x // 2 - len(text) // 2, text, curses.A_BOLD)
    user_name = read_str(stdscr, max_y // 3 + 1,
                         max_x // 2 - len(text) // 2 - 2, len(text), '>')
    try :
        return user.connection(sys.argv[1],user_name)
    except :
        exit("Serveur not found")

