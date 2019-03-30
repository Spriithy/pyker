import curses
import curses.textpad as textpad
from server import instance as server
from proxy import instance as proxy
from threading import Thread
import time

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


def pull_stats(win):
    while True:
        if proxy.stop_threads:
            break
        win.addstr(0, 0, get_statusbar(win.getmaxyx()[1]), curses.A_REVERSE)
        win.refresh()
        time.sleep(0.1)


def get_key_thread(win, stdscr):
    (max_y, max_x) = win.getmaxyx()
    while True:
        if proxy.stop_threads:
            break
        for i in range(len(tictactoe)):
            stdscr.addstr(max_y // 6 + i, max_x // 2 - len(tictactoe[i]) // 2,
                          tictactoe[i], curses.color_pair(248))
        key = stdscr.getkey()
        if key:
            win.addstr(0, 0, key)
            win.border()
        win.refresh()


def run(stdscr):
    stdscr.clear()

    (max_y, max_x) = stdscr.getmaxyx()
    mainWin = curses.newwin(max_y - 1, max_x, 1, 0)
    mainWin.refresh()

    statusWin = curses.newwin(1, max_x)
    statusWin.addstr(0, 0, '' * max_x)
    statusWin.refresh()
    thread_pull_stats = Thread(target=pull_stats, args=(statusWin, ))
    thread_pull_stats.start()
    thread_key_press = Thread(
        target=get_key_thread, args=(
            mainWin,
            stdscr,
        ))
    thread_key_press.start()
    thread_pull_stats.join()
    thread_key_press.join()
    mainWin.getch()


tictactoe = [
    '████████╗██╗ ██████╗████████╗ █████╗  ██████╗████████╗ ██████╗ ███████╗',
    "╚══██╔══╝██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔════╝",
    "   ██║   ██║██║        ██║   ███████║██║        ██║   ██║   ██║█████╗  ",
    "   ██║   ██║██║        ██║   ██╔══██║██║        ██║   ██║   ██║██╔══╝  ",
    "   ██║   ██║╚██████╗   ██║   ██║  ██║╚██████╗   ██║   ╚██████╔╝███████╗",
    "   ╚═╝   ╚═╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚══════╝",
]