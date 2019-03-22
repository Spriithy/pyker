import sys
import os
import InterfaceClass as itc
#import threading
from ApiCalls import instance_Server as api
from UserClass import user as user
from Pinger import pinger as pinger


it=itc.Interface
itc.clear()
it.standard_Print("Welcome to Pyker BB ")
user.IDs_= it.set_Addr_Serv(sys.argv[1])
api.ping_Serv()

input("END")
exit(0)
