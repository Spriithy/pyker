from uuid import uuid4
import os
import http
import time
import requests
import json
import UserClass as us
import InterfaceClass as it
#import threading

def clear():
    os.system("clear")


def thread(timeStart):
    print(timeStart)


it=it.Interface
clear()
print("Welcome to Pyker BB")
user=us.UserClass(it.print_Connexion())
it.print_Clear_WhoAmI(user.whoAmI())
it.print_Interface(user.whoAmI())
"""
me = us.UserClass()
me.cleared_whoAmI()
interface = it.Interface(me)
#interface.print_Interface()
response = (requests.get("http://0.0.0.0:5000/v0/conn/init/%s/10"% me.id_)).json()
print(response)
me.id_Hash=response["client_id"]
"""
"""while(1):
    thread(time.time())
    threading.Thread(target=ping,args=(hostname,)).start()
"""
#print_Interface()
input("END")
exit(0)
