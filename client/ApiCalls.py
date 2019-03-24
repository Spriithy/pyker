import requests
import json


class ApiCalls(object):
    def __init__(self):
        self.session = requests.Session()
        self.addrServ = "0.0.0.0"
        self.prefix = "http://0.0.0.0:5000/v0"

    def set_addr_Serv(self, addr, username):
        self.addrServ = addr
        self.prefix = "http://%s:5000/v0" % addr
        return self.connection_Init(username)

    def connection_Init(self, username):
        return ((self.session.post(
            "%s/conn/init" % (self.prefix),
            data={"user.name": "%s" % username})).json())

    def ping_Serv(self):
        return self.session.get("%s/ping" % (self.prefix)).json()

    def pull_Messages(self, last_Message):
        return self.session.get("%s/lobby/pull/messages?start=%i" %
                                (self.prefix, last_Message)).json()

    def push_Message(self, message, to='lobby'):
        return self.session.post(
            "%s/lobby/push/message" % (self.prefix),
            data={
                "message.content": "%s" % message,
                "message.to": "%s" % to
            }).json()

    def getUsers(self):
        return self.session.get("%s/conn/get/users"%self.prefix).json()
    
    def init_Table(self,name):
        return self.session.post("%s/table/init"%self.prefix, data={"table.name":"%s"%name}).json()
    
    def get_Tables(self):
        return self.session.get("%s/table/list"%self.prefix).json()

    def quit(self):
        return self.session.get('%s/conn/drop'% self.prefix).json()


instance_Server = ApiCalls()
