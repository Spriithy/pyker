import curses
import curses.textpad as textpad
from server import instance as server
from proxy import instance as proxy
from threading import Thread
import time

ip = "0.0.0.0:5000"
ping = "8 ms | "
username = "Moi#8888"
versus = " vs "
contestant = "Qqun#8664 "
score = "        score : YOU 0 - 0 HIM  "


def get_statusbar(width):
    global username
    global ping
    return username + versus + contestant + score + ' ' * (
        width - 2 - len(username) - len(versus) - len(contestant) - len(score)
        - len(ping) - len(ip)) + ping + ip + ' '

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


def pullStats(win):
    win.addstr(0, 0, get_statusbar(win.getmaxyx()[1]), curses.A_REVERSE)
    win.refresh()


def run(stdscr):
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    mainWin = curses.newwin(max_y - 2, max_x, 2, 0)
    mainWin.refresh()

    statusWin = curses.newwin(2, max_x)
    statusWin.addstr(0, 0, 'X' * max_x)
    statusWin.refresh()
    pullStatsThread = Thread(target=pullStats, args=(statusWin, ))
    pullStatsThread.start()
    pullStatsThread.join()
    mainWin.getch()