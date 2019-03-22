import random
import sys
from threading import Thread
import time
from ApiCalls import instance_Server as api
from UserClass import user as user
class Pinger(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print("oOOOOppp")
        while(True):
            user.pull_Message()
            time.sleep(10) #temps en sec

pinger=Pinger()