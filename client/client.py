import sys
import os
import InterfaceClass as itc
from ApiCalls import instance_Server as api
from UserClass import user as user
from Pinger import pinger as pinger
import curses
from curses import wrapper

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input

def main(stdscr):
    nb_Colonnes=curses.COLS
    nb_Lignes=curses.LINES

    stdscr.clear()
    stdscr.addstr(0,int(nb_Colonnes/2),"lll")
    choice = my_raw_input(stdscr, 2, 3, "cool or hot?").lower()
    stdscr.addstr(15,15,choice)
    print(type(choice))
    if str(choice) == "cool":
        stdscr.addstr(5,3,"Super cool!")
    elif choice == "hot":
        stdscr.addstr(5, 3," HOT!") 
    else:
        stdscr.addstr(5, 3," Invalid input") 


    stdscr.refresh()
    stdscr.getch()
    stdscr.getkey()


wrapper(main)

tableau =   ["",
            ""]

"""
carte=".------..------..------..------..------.
|P.--. ||Y.--. ||K.--. ||E.--. ||R.--. |
| :/\: || (\/) || :/\: || (\/) || :(): |
| (__) || :\/: || :\/: || :\/: || ()() |
| '--'P|| '--'Y|| '--'K|| '--'E|| '--'R|
`------'`------'`------'`------'`------'"
"""