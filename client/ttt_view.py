import curses
import curses.textpad as textpad
from server import instance as server
from proxy import instance as proxy
from threading import Thread
import time
import ttt_grid

ip = "0.0.0.0:5000"  #proxy.server_address
ping = "8 ms | "  #
username = "Moi#8888"  #proxy.username
versus = " vs "
contestant = "Qqun#8664 "
score = "        score : YOU 0 - 0 HIM  "


def get_statusbar(width):
    global username
    global ping
    return username + versus + contestant + score + ' ' * (
        width - 1 - len(username) - len(versus) - len(contestant) - len(score)
        - len(ping) - len(ip)) + ping + ip

    # pings = []
    # for _ in range(10):
    #     pings.append(server.ping())
    # ping = '- ms | '
    # try:
    #     ping = '%d ms | ' % (sum(pings) / 10)
    # except:
    #     pass
    # username = 'ID : %s' % proxy.username
    # return username + ' ' * (
    #     width - 2 - len(username) - len(ping) - len(ip)) + ping + ip + ' '


def pull_stats(window):
    while True:
        (max_y, max_x) = window.getmaxyx()
        if proxy.stop_threads:
            break
        window.addstr(0, 0, get_statusbar(window.getmaxyx()[1]),
                      curses.A_REVERSE)
        for i in range(len(tictactoe)):
            window.addstr(2 + i, max_x // 2 - len(tictactoe[i]) // 2,
                          tictactoe[i], curses.color_pair(3))
        window.refresh()
        time.sleep(0.1)


def get_key_thread(win, stdscr):
    (max_y, max_x) = win.getmaxyx()
    grids = [ttt_grid.Grid(), ttt_grid.Grid()]
    while True:
        win.clear()
        if proxy.stop_threads:
            break
        win.border()
        win.refresh()
        for grid in grids:
            for i in range(len(grid.graphic)):
                win.addstr(2 + i, 2 + len(grids) * 6, grid.graphic[i],
                           curses.color_pair(2))
        key = win.getkey()
        if key:
            win.addstr(0, 0, key)


def run(stdscr):
    stdscr.clear()

    (max_y, max_x) = stdscr.getmaxyx()
    mainWin = curses.newwin(max_y - 9, max_x, 9, 0)
    mainWin.refresh()

    statusWin = curses.newwin(8, max_x)

    thread_key_press = Thread(
        target=get_key_thread, args=(
            mainWin,
            stdscr,
        ))
    thread_key_press.start()
    thread_pull_stats = Thread(target=pull_stats, args=(statusWin, ))
    thread_pull_stats.start()
    thread_pull_stats.join()
    thread_key_press.join()


tictactoe = [
    '████████╗██╗ ██████╗████████╗ █████╗  ██████╗████████╗ ██████╗ ███████╗',
    "╚══██╔══╝██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔════╝",
    "   ██║   ██║██║        ██║   ███████║██║        ██║   ██║   ██║█████╗  ",
    "   ██║   ██║██║        ██║   ██╔══██║██║        ██║   ██║   ██║██╔══╝  ",
    "   ██║   ██║╚██████╗   ██║   ██║  ██║╚██████╗   ██║   ╚██████╔╝███████╗",
    "   ╚═╝   ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚══════╝",
]

game_grid = [
    " | | ",
    "-+-+-",
    " | | ",
    "-+-+-",
    " | | ",
]

