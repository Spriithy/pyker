from uuid import uuid4
import os
import http
import time
import requests
import json
from ApiCalls import instance_Server as api

class UserClass():
    def __init__(self):
        self.ID_=None

    def whoAmI(self):
        return self.ID_
    
user = UserClass()