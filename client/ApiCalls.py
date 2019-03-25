import requests
import json


class ApiCalls(object):
    def __init__(self):
        self.session = requests.Session()
        self.addrServ = "0.0.0.0"
        self.prefix = "http://0.0.0.0:5000/v0"
        self.quitted = False

    def set_addr_Serv(self, addr, username):
        if not self.quitted:
            self.addrServ = addr if len(
                addr.split(':')) == 2 else addr + ":5000"
            self.prefix = "http://%s/v0" % self.addrServ
            return (self.connection_Init(username), self.addrServ)

    def ping(self):
        return requests.get(
            '%s/conn/ping' % self.prefix).elapsed.total_seconds() / 1000

    def connection_Init(self, username):
        if not self.quitted:
            return ((self.session.post(
                "%s/conn/init" % (self.prefix),
                data={"user.name": "%s" % username})).json())

    def ping_Serv(self):
        if not self.quitted:
            return self.session.get("%s/ping" % (self.prefix)).json()

    def join_lobby(self):
        if not self.quitted:
            return self.session.get('%s/lobby/join' % self.prefix).json()

    def last_message_id(self):
        if not self.quitted:
            return self.session.get(
                '%s/lobby/last_message_id' % self.prefix).json()['int']

    def pull_Messages(self, last_Message):
        if not self.quitted:
            return self.session.get("%s/lobby/pull/messages?start=%i" %
                                    (self.prefix, last_Message)).json()

    def push_Message(self, message, to='lobby'):
        if not self.quitted:
            return self.session.post(
                "%s/lobby/push/message" % (self.prefix),
                data={
                    "message.content": "%s" % message,
                    "message.to": "%s" % to
                }).json()

    def getUsers(self):
        if not self.quitted:
            return self.session.get("%s/conn/get/users" % self.prefix).json()

    def init_Table(self, name):
        if not self.quitted:
            return self.session.post(
                "%s/table/init" % self.prefix,
                data={
                    "table.name": "%s" % name
                }).json()

    def get_Table(self):
        if not self.quitted:
            return self.session.get("%s/table/get" % self.prefix).json()

    def get_Tables(self):
        if not self.quitted:
            return self.session.get("%s/table/list" % self.prefix).json()

    def join_Table(self, name):
        if not self.quitted:
            return self.session.get("%s/table/join/%s" % (self.prefix, name))

    def leave_Table(self):
        if not self.quitted:
            return self.session.get("%s/table/leave" % (self.prefix))

    def drop_Table(self, name):
        if not self.quitted:
            return self.session.get("%s/table/drop/%s" % (self.prefix, name))

    def quit(self):
        self.quitted = True
        return self.session.get('%s/conn/drop' % self.prefix).json()


instance_Server = ApiCalls()
