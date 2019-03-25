import curses
import sys
from server import instance as server
from proxy import instance as proxy


def read_str(stdscr, y, x, n, prompt=''):
    curses.echo()
    stdscr.addstr(y, x, prompt)
    stdscr.refresh()
    text = stdscr.getstr(y, len(prompt) + 1 + x, n)
    curses.noecho()
    return str(text, 'utf-8')


def connection_Lobby(stdscr, max_y, max_x):
    stdscr.clear()
    for i in range(len(pyker)):
        stdscr.addstr(max_y // 6 + i, max_x // 2 - len(pyker[i]) // 2,
                      pyker[i], curses.color_pair(248))
    stdscr.addstr
    text = 'Type in your username'
    stdscr.addstr(max_y // 2, max_x // 2 - len(text) // 2, text, curses.A_BOLD)
    credit = '@Spriithy & @ErnestBidouille'
    stdscr.addstr(max_y - 4, max_x // 2 - len(credit) // 2, credit,
                  curses.color_pair(6))
    user_name = read_str(stdscr, max_y // 2 + 1,
                         max_x // 2 - len(text) // 2 - 2, len(text), '>')
    try:
        return proxy.connection(sys.argv[1], user_name)
    except:
        exit("Server connection failed")


pyker = [
    '██████╗ ██╗   ██╗██╗  ██╗███████╗██████╗ ',
    '██╔══██╗╚██╗ ██╔╝██║ ██╔╝██╔════╝██╔══██╗',
    '██████╔╝ ╚████╔╝ █████╔╝ █████╗  ██████╔╝',
    '██╔═══╝   ╚██╔╝  ██╔═██╗ ██╔══╝  ██╔══██╗',
    '██║        ██║   ██║  ██╗███████╗██║  ██║',
    '╚═╝        ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝',
]
