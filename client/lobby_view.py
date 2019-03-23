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
                           (w - 3 - len(lines_str) - len(ip) - 1), ip)

def pull_Thread(window) : 
    (max_y,max_x) = window.getmaxyx()
    lines=[]
    window.clear()
    while (True):
        for message in user.pull_Message():
            lines.append(fmt_message(message))
        for i in range(len(lines)):
            window.addstr(i, 0, lines[i])
        window.refresh()
        time.sleep(0.1)  #temps en sec

def run(stdscr):
    stdscr.clear()
    (max_y, max_x) = stdscr.getmaxyx()
    begin_x = 0; begin_y = 0
    height = max_y-3; width = max_x
    
    #creation de la window de thread_Pull
    thread_Win = curses.newwin(height, width, begin_y, begin_x)
    #a changer peut etre v
    curses.curs_set(0)
    thread_Win.border()

    #creation window de statubar
    message_Win = curses.newwin(2,max_x,height+1,0)
    message_Win.border()

    Thread(target=pull_Thread, args=(thread_Win,)).start()

    while True:
        message_Win.addstr(0, 0, get_statusbar(max_x), curses.A_REVERSE)
        editwin = curses.newwin(1, max_x, max_y - 1, 0)
        box = textpad.Textbox(editwin)
        message_Win.refresh()
        box.edit()
        text = box.gather().strip()
        if len(text) == 0:
            continue
        user.push_Message(text)
