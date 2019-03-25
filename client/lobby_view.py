import curses
import curses.textpad as textpad
from UserClass import user
from ApiCalls import instance_Server as api
from threading import Thread
import time

ip = ''

FROM_WHISPER = 1
TO_WHISPER = 2
SERVER_INFO = 3
SERVER_WARNING = 4
SERVER_ERROR = 5


def fmt_message(message, user):
    if message['to'] == user and '#' in message['from']:
        return '[%s][%s] said: %s' % (message['date'], message['from'],
                                      message['content']), FROM_WHISPER

    if message['from'] == user and message['to'] != 'lobby':
        return '[%s][%s]: %s' % (message['date'], message['to'],
                                 message['content']), TO_WHISPER

    msg = None
    from_ = message['from']
    if from_.split(':')[0] == 'Standalone':
        msg = '[%s] %s' % (message['date'], message['content'])
        from_ = from_.split(':')[1]
    else:
        msg = '[%s][%s]: %s' % (message['date'], from_, message['content'])

    return msg, {
        'Info': SERVER_INFO,
        'Warning': SERVER_WARNING,
        'Error': SERVER_ERROR,
    }.get(from_, curses.A_NORMAL)


def get_color_for_message(mtype):
    return [
        curses.A_NORMAL,
        curses.color_pair(5),
        curses.color_pair(5),
        curses.A_NORMAL,
        curses.color_pair(3),
        curses.color_pair(1),
    ][mtype]


def get_statusbar(w):
    pings = []
    for _ in range(10):
        pings.append(api.ping())
    ping = '- ms | '
    try:
        ping = '%d ms | ' % (sum(pings) / 10)
    except:
        pass
    username = 'ID : %s#%s' % (user.IDs_[0], user.IDs_[1])
    return username + ' ' * (
        w - 2 - len(username) - len(ping) - len(ip)) + ping + ip + ' '


def pull_Thread(windowPull, windowUsers, windowTable, windowMessage):
    users = []
    usersOld = []
    tables = []
    tablesOld = []
    lines = []
    windowPull.clear()

    while True:
        windowMessage.addstr(0, 0, get_statusbar(windowMessage.getmaxyx()[1]),
                             curses.A_REVERSE)
        (max_y, max_x) = windowPull.getmaxyx()
        if user.stop_threads:
            break
        username = '%s#%s' % (user.IDs_[0], user.IDs_[1])
        #reception et affichage des messages
        messages_pulled = user.pull_Message()
        if len(messages_pulled) > 0:
            for message in messages_pulled:
                message, mtype = fmt_message(message, username)
                if len(message) > max_x - 2:
                    while (len(message) > max_x - 2):
                        addLine = message[:max_x - 2]
                        lines.append([addLine, mtype])
                        message = message[max_x - 2:]
                    lines.append([message, mtype])
                else:
                    lines.append([message, mtype])

            windowPull.clear()
            scroller = 0 if (len(lines) - max_y + 1) <= 0 else (
                len(lines) - max_y + 1)

            for i in range(len(lines) - scroller):
                if lines[i + scroller][1] != curses.A_NORMAL:
                    windowPull.addstr(
                        i, 0, lines[i + scroller][0],
                        get_color_for_message(lines[i + scroller][1]))
                else:
                    windowPull.addstr(i, 0, lines[i + scroller][0])
            windowPull.refresh()

        #reception et affichage des users connectés
        for userConnected in user.getUsers():
            users.append(userConnected)
        if users != usersOld:
            windowUsers.clear()
            windowUsers.border()
            windowUsers.addstr(0, 1, "Connected users")
            loop = windowUsers.getmaxyx()[0] - 3
            if len(users) <= loop:
                loop = len(users)
            else:
                windowUsers.addstr(loop + 1, 1, "...")
            for i in range(loop):
                if users[i] == user.username():
                    windowUsers.addstr(i + 1, 1, users[i],
                                       curses.color_pair(3))
                else:
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
            loop = windowTable.getmaxyx()[0] - 3
            if len(tables) <= loop:
                loop = len(tables)
            else:
                windowTable.addstr(loop + 1, 1, "...")
            user_table = user.getTable()
            windowTable_max_x = windowTable.getmaxyx()[1]
            for i in range(loop):
                table_name = tables[i]['name']
                if table_name == user_table:
                    windowTable.addstr(i + 1, 1,
                                       '[*]' + ' ' * (windowTable_max_x - 5),
                                       curses.A_REVERSE)
                windowTable.addstr(
                    i + 1, 5, table_name, curses.A_REVERSE
                    if table_name == user_table else curses.A_NORMAL)
                windowTable.addstr(
                    i + 1, 6 + len(table_name),
                    '(%d)' % len(tables[i]['users']), curses.A_REVERSE
                    if table_name == user_table else curses.A_NORMAL)
            windowTable.refresh()
            tablesOld = tables
        tables = []

        windowMessage.addstr(0, 0, get_statusbar(windowMessage.getmaxyx()[1]),
                             curses.A_REVERSE)
        windowMessage.refresh()

        time.sleep(1)  #temps en sec


def run(stdscr):
    global ip
    ip = user.addrServ
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    width_col_usersCo = 30
    begin_x = 0
    begin_y = 0
    height = max_y - 2
    width = max_x - width_col_usersCo

    #a changer peut etre v
    curses.curs_set(0)

    #creation de la window de thread_Pull
    thread_Wind = curses.newwin(height, width, begin_y, begin_x)
    thread_Wind.refresh()

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

    #on run le Thread des pull messages
    threadPulling = Thread(
        target=pull_Thread,
        args=(
            thread_Wind,
            threadUSers_win,
            threadTables_win,
            message_Win,
        ))
    threadPulling.start()
    while True:
        message_Win.addstr(0, 0, get_statusbar(max_x), curses.A_REVERSE)
        message_Win.addstr(1, 0, '$ ')
        message_Win.refresh()
        editwin = curses.newwin(1, max_x, max_y - 1, 2)
        box = textpad.Textbox(editwin)
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue

        if user.push_Message(text) == 'quit':
            user.quit()
            threadPulling.join()
            exit(0)
