import curses
import curses.textpad as textpad
from UserClass import user
from threading import Thread
import time

lines = []
ip = '127.0.0.1:5000'


def fmt_message(message):
    return '%s <%s> %s' % (message['date'], message['from'],
                           message['content'])


def get_statusbar(w):
    lines_str = '%d' % len(lines)
    return '   %s %s%s ' % (user.IDs_[0], ' ' * (w - 3 - len(ip) - 10), ip)


def pull_Thread(windowPull, windowUsers, windowTable):
    (max_y, max_x) = windowPull.getmaxyx()
    lines = []
    users = []
    usersOld = []
    tables = []
    tablesOld = []
    #myTables = []
    #myTablesOld = []
    windowPull.clear()

    while (True):
        if user.stop_threads:
            break
        #reception et affichage des messages
        for message in user.pull_Message():
            message = fmt_message(message)
            if len(message) > max_x - 2:
                while (len(message) > max_x - 2):
                    addLine = message[:max_x - 2]
                    lines.append(addLine)
                    message = message[max_x - 2:]
                lines.append(message)
            else:
                lines.append(message)
        for i in range(len(lines)):

            windowPull.addstr(i + 1, 0, lines[i])
        windowPull.border()
        windowPull.addstr(0, 0, "Chat")
        windowPull.refresh()

        #reception et affichage des users connectés
        for userConnected in user.getUsers():
            users.append(userConnected)
        if users != usersOld:
            windowUsers.clear()
            windowUsers.border()
            windowUsers.addstr(0, 1, "Connected users")
            for i in range(len(users)):
                windowUsers.addstr(i + 1, 1, users[i])
            windowUsers.refresh()
            usersOld = users
        users = []

        #reception et affichages tables de jeu
        for tableCreated in user.getTables():
            tables.append(tableCreated)
        if tables != tablesOld:
            windowTable.clear()
            windowTable.border()
            windowTable.addstr(0, 1, "Tables")
            for i in range(len(tables)):
                windowTable.addstr(i + 1, 1, tables[i])
            windowTable.refresh()
            tablesOld = tables
        tables = []
        """
        #affichage des myTables actives
        for myTables in user.getMyTables():
            myTables.append(myTables)
        if myTables != myTablesOld:
            windowMyTables.clear()
            windowMyTables.border()
            windowMyTables.addstr(0, 0, "MyTables")
            for i in range(len(myTables)):
                #changer le add str et trouver bon format
                windowMyTables.addstr(1, i + 5, myTables[i])
            windowMyTables.refresh()
            myTablesOld = myTables
        myTables = []
        """
        time.sleep(1)  #temps en sec


def run(stdscr):
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    width_col_usersCo = 20
    begin_x = 0
    begin_y = 0
    height = max_y - 2
    width = max_x - width_col_usersCo

    #a changer peut etre v
    curses.curs_set(0)

    #creation de la window de thread_Pull
    thread_Wind = curses.newwin(height, width, begin_y, begin_x)
    thread_Wind.border()
    thread_Wind.addstr(0, 0, "Chat")
    thread_Wind.refresh()
    """
    #creation windows tables en cours
    threadMyTables_Win = curses.newwin(3, width, height - 3, 0)
    threadMyTables_Win.border()
    threadMyTables_Win.addstr(0, 0, "MyTables")
    threadMyTables_Win.refresh()
    """
    #creation window de statubar
    message_Win = curses.newwin(2, max_x, height, 0)
    # message_Win.border()
    message_Win.refresh()

    #creation de la windows de thread_users
    threadUSers_win = curses.newwin(
        int(max_y / 2), width_col_usersCo, 0, width)
    threadUSers_win.border()
    threadUSers_win.addstr(0, 1, "Connected users")
    threadUSers_win.refresh()

    #creation de la windows de thread_tables
    threadTables_win = curses.newwin(
        int(max_y / 2 - 1.5), width_col_usersCo, int(max_y / 2), width)
    threadTables_win.border()
    threadTables_win.addstr(0, 1, "Tables")
    threadTables_win.refresh()

    #a enlever after debug
    threadTables_win.getch()

    #on run le Thread des pull messages
    threadPulling = Thread(
        target=pull_Thread,
        args=(
            thread_Wind,
            threadUSers_win,
            threadTables_win,
        ))
    threadPulling.start()
    while True:
        message_Win.addstr(0, 0, get_statusbar(max_x), curses.A_REVERSE)
        message_Win.addstr(1, 0, ">")
        editwin = curses.newwin(1, max_x, max_y - 1, 1)
        box = textpad.Textbox(editwin)
        message_Win.refresh()
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue
        user.push_Message(text)
