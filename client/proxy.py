from server import instance as server


class PykerProxy():
    def __init__(self):
        self.IDs_ = None
        self.last_Message = 0
        self.stop_threads = False
        self.addrServ = None

    def whoAmI(self):
        return self.IDs_

    def username(self):
        return '%s#%s' % (self.IDs_[0], self.IDs_[1])

    def pull_Message(self):
        if not self.last_Message:
            self.last_Message = server.last_message_id() - 1
        messages_Pulled = server.pull_Messages(self.last_Message)
        self.last_Message = server.last_message_id()
        return messages_Pulled["lobby.messages"]

    def push_Message(self, message, to='lobby'):
        if len(message.strip()) == 0:
            return False
        if message[0] in ['-', '!', '.', '/']:
            message_splited = message[1:].split()
            try:
                if message_splited[0] in ('w', 'whisp', 'whisper'):
                    to = message_splited[1]
                    cut = len(message_splited[0] + message_splited[1]) + 2
                    message = message[cut:].strip()
                    if len(message.strip()) == 0:
                        return

                elif message_splited[0] in ('t', 'table'):
                    return server.init_Table(message_splited[1])

                elif message_splited[0] in ('j', 'join'):
                    return server.join_Table(message_splited[1])

                elif message_splited[0] in ('l', 'leave'):
                    return server.leave_Table()

                elif message_splited[0] in ('d', 'drop'):
                    return server.drop_Table(message_splited[1])

                elif message_splited[0] in ('q', 'quit', 'exit'):
                    return 'quit'
            except:
                pass

        response = server.push_Message(message, to)
        return response, response['status'] == 'OK'

    def ping_Serv(self):
        return ((server.ping_Serv())["action"])

    def connection(self, address, username):
        username = username.replace(" ", "")
        if username == "":
            username = "Anonymous"
        retour_connection, self.addrServ = server.set_addr_Serv(
            address, username)
        if retour_connection["status"] == "OK":
            self.IDs_ = [
                retour_connection["user.name"], retour_connection["user.id"]
            ]
            return self.ping_Serv()
        return False

    def getUsers(self):
        return server.getUsers()["user.list"]

    def getTable(self):
        return server.get_Table()['str']

    def getTables(self):
        return server.get_Tables()["table.list"]

    def quit(self):
        self.stop_threads = True
        server.leave_Table()
        return server.quit()


instance = PykerProxy()
