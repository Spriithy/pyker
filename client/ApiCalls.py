from uuid import uuid4
import os
import http
import time
import requests
import json
import socket

class ApiCalls(object):

    def __init__(self):
        self.hostname = socket.gethostname()    
        self.IPAddr = str(socket.gethostbyname(self.hostname))
        self.addrServ= "0.0.0.0"
        self.prefix="http://0.0.0.0:5000/v0"

    def set_addr_Serv(self,addr):
        self.addrServ=addr
        self.prefix = "http://%s:5000/v0"%addr
        return self.pingServ()

    def pingServ(self):
        return (requests.get("%s/conn/ping"%(self.prefix))).json()

    def connexion(self,name):
        return (requests.get("%s/conn/init/%s/10/%s"% (self.prefix,self.IPAddr,name))).json()


instance_Server = ApiCalls()

