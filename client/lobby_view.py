import curses
import curses.textpad as textpad
from server import instance as server
from proxy import instance as proxy
from threading import Thread
import time

FROM_WHISPER = 1
TO_WHISPER = 2
SERVER_INFO = 3
SERVER_WARNING = 4
SERVER_ERROR = 5

lines = []


def get_message_format(message, user):
    if message['to'] == user and '#' in message['from']:
        return '[%s][%s] said: %s' % (message['date'], message['from'],
                                      message['content']), FROM_WHISPER

    if message['from'] == user and message['to'] != 'lobby':
        return '[%s][%s]: %s' % (message['date'], message['to'],
                                 message['content']), TO_WHISPER

    text = None
    from_ = message['from']
    if from_.split(':')[0] == 'Standalone':
        text = '[%s] %s' % (message['date'], message['content'])
        from_ = from_.split(':')[1]
    else:
        text = '[%s][%s]: %s' % (message['date'], from_, message['content'])

    return text, {
        'Info': SERVER_INFO,
        'Warning': SERVER_WARNING,
        'Error': SERVER_ERROR,
    }.get(from_, curses.A_NORMAL)


def get_display_for_message_type(message_type):
    return [
        curses.A_NORMAL,
        curses.color_pair(5),
        curses.color_pair(5),
        curses.A_NORMAL,
        curses.color_pair(3),
        curses.color_pair(1),
    ][message_type]


def get_statusbar(width):
    pings = []
    for _ in range(10):
        pings.append(server.ping())
    ping = '- ms | '
    try:
        ping = '%d ms | ' % (sum(pings) / 10)
    except:
        pass
    username = 'ID : %s' % proxy.username
    return username + ' ' * (
        width - 2 - len(username) - len(ping) - len(ip)) + ping + ip + ' '


def pull(chat_win, users_win, tables_win, statusbar_win):

    global lines
    users = []
    prev_users = []
    tables = []
    prev_tables = []
    lines = []
    chat_win.clear()

    while True:
        statusbar_win.addstr(0, 0, get_statusbar(statusbar_win.getmaxyx()[1]),
                             curses.A_REVERSE)
        (ymax, xmax) = chat_win.getmaxyx()
        if proxy.stop_threads:
            break
        #reception et affichage des messages
        pulled_messages = proxy.pull_messages()
        if len(pulled_messages) > 0:
            for message in pulled_messages:
                message, message_type = get_message_format(
                    message, proxy.username)
                if len(message) > xmax - 2:
                    while (len(message) > xmax - 2):
                        temp_line = message[:xmax - 2]
                        lines.append([temp_line, message_type])
                        message = message[xmax - 2:]
                    lines.append([message, message_type])
                else:
                    lines.append([message, message_type])

            chat_win.clear()
            scroller = 0 if (len(lines) - ymax + 1) <= 0 else (
                len(lines) - ymax + 1)

            for i in range(len(lines) - scroller):
                if lines[i + scroller][1] != curses.A_NORMAL:
                    chat_win.addstr(
                        i, 0, lines[i + scroller][0],
                        get_display_for_message_type(lines[i + scroller][1]))
                else:
                    chat_win.addstr(i, 0, lines[i + scroller][0])
            chat_win.refresh()

        #reception et affichage des users connectés
        for user in proxy.get_users():
            users.append(user)

        if users != prev_users:
            users_win.clear()
            users_win.border()
            users_win.addstr(0, 1, 'Connected users')
            loop = users_win.getmaxyx()[0] - 3
            if len(users) <= loop:
                loop = len(users)
            else:
                users_win.addstr(loop + 1, 1, '...')
            for i in range(loop):
                if users[i] == proxy.username:
                    users_win.addstr(i + 1, 1, users[i], curses.color_pair(3))
                else:
                    users_win.addstr(i + 1, 1, users[i])

            users_win.refresh()
            prev_users = users
        users = []

        #reception et affichages tables de jeu
        for table in proxy.get_tables():
            tables.append(table)

        if tables != prev_tables:
            tables_win.clear()
            tables_win.border()
            tables_win.addstr(0, 1, 'Tables')
            loop = tables_win.getmaxyx()[0] - 3
            if len(tables) <= loop:
                loop = len(tables)
            else:
                tables_win.addstr(loop + 1, 1, '...')
            user_table = proxy.get_user_table()
            tables_win_xmax = tables_win.getmaxyx()[1]
            for i in range(loop):
                table_name = tables[i]['name']
                if table_name == user_table:
                    tables_win.addstr(i + 1, 1,
                                      '[*]' + ' ' * (tables_win_xmax - 5),
                                      curses.A_REVERSE)
                tables_win.addstr(
                    i + 1, 5, table_name, curses.A_REVERSE
                    if table_name == user_table else curses.A_NORMAL)
                tables_win.addstr(
                    i + 1, 6 + len(table_name),
                    '(%d)' % len(tables[i]['users']), curses.A_REVERSE
                    if table_name == user_table else curses.A_NORMAL)
            tables_win.refresh()
            prev_tables = tables
        tables = []
        statusbar_win.addstr(0, 0, get_statusbar(statusbar_win.getmaxyx()[1]),
                             curses.A_REVERSE)
        statusbar_win.refresh()
        time.sleep(0.1)


def run(stdscr):
    global ip
    ip = proxy.server_address
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    column_width = 30
    begin_x = 0
    begin_y = 0
    height = max_y - 2
    width = max_x - column_width

    #a changer peut etre v
    curses.curs_set(0)

    #creation de la window de thread_Pull
    chat_win = curses.newwin(height, width, begin_y, begin_x)
    chat_win.refresh()

    #creation window de statubar
    status_win = curses.newwin(2, max_x, height, 0)
    # message_Win.border()
    status_win.refresh()

    #creation de la windows de thread_users
    users_win = curses.newwin(int(max_y / 2), column_width, 0, width)
    users_win.border()
    users_win.addstr(0, 1, 'Connected users')
    users_win.refresh()

    #creation de la windows de thread_tables
    tables_win = curses.newwin(
        int(max_y / 2 - 1.5), column_width, int(max_y / 2), width)
    tables_win.border()
    tables_win.addstr(0, 1, 'Tables')
    tables_win.refresh()

    #on run le Thread des pull messages
    pull_thread = Thread(
        target=pull, args=(
            chat_win,
            users_win,
            tables_win,
            status_win,
        ))
    pull_thread.start()
    while True:
        status_win.addstr(0, 0, get_statusbar(max_x), curses.A_REVERSE)
        status_win.addstr(1, 0, '$ ')
        status_win.refresh()
        editwin = curses.newwin(1, max_x, max_y - 1, 2)
        box = textpad.Textbox(editwin)
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue
        message = proxy.push_message(text)
        if message == 'quit':
            proxy.quit()
            pull_thread.join()
            exit(0)
        elif message == 'clear':
            global lines
            lines = []
            chat_win.clear()
            chat_win.refresh()
