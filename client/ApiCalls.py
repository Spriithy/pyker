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

    def set_addr_Serv(self,addr,username):
        self.addrServ=addr
        self.prefix = "http://%s:5000/v0"%addr
        return self.connexion_Init(username)

    def connexion_Init(self,username):
        return((requests.post("%s/conn/init"% (self.prefix),data={"user.name":"%s"%username})).json())

instance_Server = ApiCalls()

