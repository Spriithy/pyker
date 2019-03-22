from uuid import uuid4
import os
import http
import time
import requests
import json
from ApiCalls import instance_Server as api

class UserClass():
    def __init__(self,name):
        self.user_=api.connexion(name)

    def whoAmI(self):
        return self.user_["client_name"]
    
    def getMyID(self):
        return self.user_["client_id"]