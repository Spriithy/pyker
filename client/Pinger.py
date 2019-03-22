import time
from threading import Thread
from UserClass import user as user

class Pinger(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while(True):
            print(user.pull_Message())
            time.sleep(0.1) #temps en sec

pinger=Pinger()