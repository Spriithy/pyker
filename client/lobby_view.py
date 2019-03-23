import curses
import curses.textpad as textpad
import signal
import sys
from UserClass import user
from threading import Thread
import time

is_active=True
signal.signal(signal.SIGINT, lambda x, y: (sys.exit(0)))

lines = []
ip = '127.0.0.1:5000'
    
def fmt_message(message):
    return '%s <%s> %s' % (message['date'], message['from'],
                           message['content'])


def get_statusbar(w):
    lines_str = '%d' % len(lines)
    return '   %s%s%s ' % (lines_str, ' ' *
                           (w - 3 - len(lines_str) - len(ip) - 10), ip)
    return '   %s%s ' % (ip, ' ' *( w-3-len(ip)-30))

def pull_Thread(windowPull, windowUsers, windowTable) : 
    (max_y,max_x) = windowPull.getmaxyx()
    lines=[]
    users=[]
    windowPull.clear()
    while (True):
        for message in user.pull_Message():
            lines.append(fmt_message(message))
        for i in range(len(lines)):
            windowPull.addstr(i, 0, lines[i])

        windowPull.refresh()
        windowUsers.clear()
        windowUsers.addstr(0,1,"Users co")
        for userConnected in user.getUsers():
            users.append(userConnected)
        for i in range(len(users)):
            windowUsers.addstr(i+1,1,users[i])
        windowUsers.refresh()
        users=[]
        time.sleep(5)  #temps en sec

def run(stdscr):
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    begin_x = 0; begin_y = 0
    height = max_y-3; width = max_x-15
    
    #a changer peut etre v
    curses.curs_set(0)
    #creation de la window de thread_Pull
    thread_Wind = curses.newwin(height, width, begin_y, begin_x)
    thread_Wind.border()
    # (max_yi,max_xi) = thread_Wind.getmaxyx()
    # thread_Wind.addstr(0, 0, str(max_yi)+' '+str(max_xi))
    # thread_Wind.addstr(max_yi-2, max_xi-2, "X")
    # thread_Wind.addstr(max_yi-2, 0, "X")
    # thread_Wind.addstr(0, max_xi-2, "X")
    thread_Wind.refresh()
    #creation window de statubar
    message_Win = curses.newwin(2,max_x,height,0)
    message_Win.border()
    # (max_yi,max_xi) = message_Win.getmaxyx()
    # message_Win.addstr(0, 0, str(max_yi)+' '+str(max_xi))
    
    # message_Win.addstr(max_yi-2, max_xi-2, "M")
    # message_Win.addstr(max_yi-2, 0, "M")
    # message_Win.addstr(0, max_xi-2, "M")

    message_Win.refresh()
    #creation window de s
    #creation de la windows de thread_users
    threadUSers_win = curses.newwin(int(max_y/2),15,0,width)
    threadUSers_win.border()
    # (max_yi,max_xi) = threadUSers_win.getmaxyx()
    # threadUSers_win.addstr(0, 0, str(max_yi)+' '+str(max_xi))
    # threadUSers_win.addstr(max_yi-2, max_xi-2, "S")
    # threadUSers_win.addstr(max_yi-2, 0, "S")
    # threadUSers_win.addstr(0, max_xi-2, "S")
    threadUSers_win.refresh()
    #creation de la windows de thread_tables
    threadTables_win = curses.newwin(int(max_y/2-4),15,int(max_y/2),width)
    threadTables_win.border()
    # (max_yi,max_xi) = threadUSers_win.getmaxyx()
    # threadTables_win.addstr(0, 0, str(max_yi)+' '+str(max_xi))
    # threadTables_win.addstr(max_yi-2, max_xi-2, "O")
    # threadTables_win.addstr(max_yi-2, 0, "O")
    # threadTables_win.addstr(0, max_xi-2, "O")
    threadTables_win.refresh()
    threadTables_win.getch()

    #on run le Thread des pull messages
    Thread(target=pull_Thread, args=(thread_Wind,threadUSers_win,threadTables_win,)).start()

    while True:
        message_Win.addstr(0, 0, get_statusbar(max_x), curses.A_REVERSE)
        editwin = curses.newwin(1, max_x, max_y, 0)
        box = textpad.Textbox(editwin)
        message_Win.refresh()
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue
        user.push_Message(text)
