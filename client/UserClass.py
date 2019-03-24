from ApiCalls import instance_Server as api


class UserClass():
    def __init__(self):
        self.IDs_ = None
        self.last_Message = 0
        self.stop_threads = False

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
        if message[0] in ['-', '!', '.', '/']:
            message_splited = message.split()
            try:
                if message_splited[0] == message[0] + "w":
                    to = message_splited[1]
                    cut = len(message_splited[0] + message_splited[1]) + 2
                    message = to + ": " + message[cut:]

                elif message_splited[0] == message[0] + "t":
                    return api.init_Table(message_splited[1])

                elif message_splited[0] == message[0] + "j":
                    return api.join_Table(message_splited[1])

                elif message_splited[0] == message[0] + "l":
                    return api.leave_Table()

                elif message_splited[0] == message[0] + "d":
                    return api.drop_Table(message_splited[1])

                elif message_splited[0] == message[0] + "q":
                    api.quit()
                    exit("Deconnecté")
            except:
                pass
        return api.push_Message(message, to)["status"] == "OK"

    def ping_Serv(self):
        return ((api.ping_Serv())["action"])

    def connection(self, address, username):
        username = username.replace(" ", "")
        if username == "":
            username = "Anonymous"
        retour_connection = api.set_addr_Serv(address, username)
        if retour_connection["status"] == "OK":
            self.IDs_ = [
                retour_connection["user.name"], retour_connection["user.id"]
            ]
            return self.ping_Serv()
        return False

    def getUsers(self):
        return api.getUsers()["user.list"]

    def getTables(self):
        return api.get_Tables()["table.list"]

    def quit(self):
        self.stop_threads = True
        return api.quit()


user = UserClass()