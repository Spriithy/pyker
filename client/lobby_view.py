import curses
import curses.textpad as textpad
import signal
import sys
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
    return '   %s %s%s%s ' % (lines_str, user.IDs_[0], ' ' *
                           (w - 3 - len(lines_str) - len(ip) - 10), ip)

def pull_Thread(windowPull, windowUsers, windowTable) : 
    (max_y,max_x) = windowPull.getmaxyx()
    lines=[]
    users=[]
    tables=[]
    windowPull.clear()
    windowTable.clear()
    while (True):
        for message in user.pull_Message():
            lines.append(fmt_message(message))
        for i in range(len(lines)):
            windowPull.addstr(i+1, 0, lines[i])
        windowPull.border()
        windowPull.addstr(0, 0, "Chat")
        windowPull.refresh()
        windowUsers.clear()
        windowUsers.border()
        windowUsers.addstr(0,1,"Connected users")
        for userConnected in user.getUsers():
            users.append(userConnected)
        for i in range(len(users)):
            windowUsers.addstr(i+1,1,users[i])
        windowUsers.refresh()
        users=[]

        for tableCreated in user.getTables():
            tables.append(tableCreated)
        for i in range(len(tables)):
            windowTable.addstr(i+1,1,tables[i])
        tables=[]


        windowTable.border()
        windowTable.addstr(0,1,"Tables")
        windowTable.refresh()
        time.sleep(5)  #temps en sec

def run(stdscr):
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    width_col_usersCo = 20
    begin_x = 0; begin_y = 0
    height = max_y-2; width = max_x-width_col_usersCo
    
    #a changer peut etre v
    curses.curs_set(0)

    #creation de la window de thread_Pull
    thread_Wind = curses.newwin(height, width, begin_y, begin_x)
    thread_Wind.border()
    thread_Wind.refresh()

    #creation window de statubar
    message_Win = curses.newwin(2,max_x,height,0)
    # message_Win.border()
    message_Win.refresh()
    
    #creation de la windows de thread_users
    threadUSers_win = curses.newwin(int(max_y/2),width_col_usersCo,0,width)
    threadUSers_win.border()
    threadUSers_win.refresh()
    
    #creation de la windows de thread_tables
    threadTables_win = curses.newwin(int(max_y/2-1.5),width_col_usersCo,int(max_y/2),width)
    threadTables_win.border()
    threadTables_win.refresh()
    
    #a enlever after debug
    threadTables_win.getch()

    #on run le Thread des pull messages
    Thread(target=pull_Thread, args=(thread_Wind,threadUSers_win,threadTables_win,)).start()

    while True:
        message_Win.addstr(0, 0, get_statusbar(max_x), curses.A_REVERSE)
        message_Win.addstr(1, 0, ">")
        editwin = curses.newwin(1, max_x, max_y-1, 1)
        box = textpad.Textbox(editwin)
        message_Win.refresh()
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue
        user.push_Message(text)
