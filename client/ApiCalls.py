from uuid import uuid4
import os
import http
import time
import requests
import json
import socket

hostname = socket.gethostname()    
IPAddr = str(socket.gethostbyname(hostname))

class ApiCalls(object):
    @staticmethod
    def connexion(name):
        return (requests.get("http://0.0.0.0:5000/v0/conn/init/%s/10/%s"% (IPAddr,name))).json()

