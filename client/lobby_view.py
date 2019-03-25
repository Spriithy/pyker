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


def pull(chat_win, users_win, rooms_win, statusbar_win):
    users = []
    prev_users = []
    rooms = []
    prev_rooms = []
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
            users_win.addstr(0, 1, '[ Users ]')
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

        #reception et affichages rooms de jeu
        for room in proxy.get_rooms():
            rooms.append(room)

        if rooms != prev_rooms:
            rooms_win.clear()
            rooms_win.border()
            rooms_win.addstr(0, 1, '[ Rooms ]')
            loop = rooms_win.getmaxyx()[0] - 3
            if len(rooms) <= loop:
                loop = len(rooms)
            else:
                rooms_win.addstr(loop + 1, 1, '...')
            user_room = proxy.get_user_room()
            rooms_win_xmax = rooms_win.getmaxyx()[1]
            for i in range(loop):
                room_name = rooms[i]['name']
                if room_name == user_room:
                    rooms_win.addstr(i + 1, 1,
                                     '[*]' + ' ' * (rooms_win_xmax - 5),
                                     curses.A_REVERSE)
                rooms_win.addstr(
                    i + 1, 5, room_name, curses.A_REVERSE
                    if room_name == user_room else curses.A_NORMAL)
                rooms_win.addstr(
                    i + 1, 6 + len(room_name), '(%d)' % len(rooms[i]['users']),
                    curses.A_REVERSE
                    if room_name == user_room else curses.A_NORMAL)
            rooms_win.refresh()
            prev_rooms = rooms
        rooms = []
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
    users_win.addstr(0, 1, '[ Users ]')
    users_win.refresh()

    #creation de la windows de thread_rooms
    rooms_win = curses.newwin(
        int(max_y / 2 - 1.5), column_width, int(max_y / 2), width)
    rooms_win.border()
    rooms_win.addstr(0, 1, '[ Rooms ]')
    rooms_win.refresh()

    #on run le Thread des pull messages
    pull_thread = Thread(
        target=pull, args=(
            chat_win,
            users_win,
            rooms_win,
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

        if proxy.push_message(text) == 'quit':
            proxy.quit()
            pull_thread.join()
            exit(0)
