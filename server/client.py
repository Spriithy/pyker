from uuid import uuid4
import random


class Client(object):
    def __init__(self, ip, port, client_id):
        self.ip = ip
        self.port = port
        self.client_id = client_id
        self.user_name = ''
        self.user_id = random.randint(1000, 9999)
