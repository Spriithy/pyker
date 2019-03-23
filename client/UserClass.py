from ApiCalls import instance_Server as api


class UserClass():
    def __init__(self):
        self.IDs_ = None
        self.last_Message = 0

    def whoAmI(self):
        return self.IDs_

    def pull_Message(self):
        messages_Pulled = api.pull_Messages(self.last_Message)
        self.last_Message = self.last_Message + len(
            messages_Pulled["lobby.messages"])
        return messages_Pulled["lobby.messages"]

    def push_Message(self, message, to='lobby'):
        if (len(message.strip()) == 0):
            return False
        return api.push_Message(message, to)["status"] == "OK"

    def ping_Serv(self):
        return ((api.ping_Serv())["action"])

    def connection(self, address, username):
        retour_connection = api.set_addr_Serv(address, username)
        if retour_connection["status"] == "OK":
            self.IDs_ = [
                retour_connection["user.name"], retour_connection["user.id"]
            ]
            return self.ping_Serv()
        return False


user = UserClass()