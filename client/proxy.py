from server import instance as server


class PykerProxy(object):
    def __init__(self):
        self.username = None
        self.last_message_id = 0
        self.stop_threads = False
        self.server_address = None

    def pull_messages(self):
        if not self.last_message_id:
            self.last_message_id = server.last_message_id() - 1
        pulled = server.pull_messages(self.last_message_id)
        self.last_message_id = server.last_message_id()
        return pulled['lobby.messages']

    def push_message(self, message, to='lobby'):
        if len(message.strip()) == 0:
            return False
        if message[0] in ['-', '!', '.', '/']:
            message_parts = message[1:].split()
            try:
                if message_parts[0] in ('w', 'whisp', 'whisper'):
                    to = message_parts[1]
                    cut = len(message_parts[0] + message_parts[1]) + 2
                    message = message[cut:].strip()
                    if len(message.strip()) == 0:
                        return

                elif message_parts[0] in ('t', 'table'):
                    return server.init_table(message_parts[1])

                elif message_parts[0] in ('j', 'join'):
                    return server.join_table(message_parts[1])

                elif message_parts[0] in ('l', 'leave'):
                    return server.leave_table()

                elif message_parts[0] in ('d', 'drop'):
                    return server.drop_table(message_parts[1])

                elif message_parts[0] in ('q', 'quit', 'exit'):
                    return 'quit'

                elif message_parts[0] in ('c', 'clear'):
                    self.last_message_id = server.last_message_id()
                    return "clear"

            except:
                pass

        response = server.push_message(message, to)
        return response, response['status'] == 'OK'

    def ping_action(self):
        return ((server.ping_action())['action'])

    def connect(self, address, user):
        user = user.replace(' ', '')
        if len(user) == 0:
            user = 'Anonymous'
        response, self.server_address = server.set_addr_serv(address, user)
        if response['status'] == 'OK':
            self.username = '%s#%s' % (response['user.name'],
                                       response['user.id'])
            return self.ping_action()
        return False

    def get_users(self):
        return server.get_users()['user.list']

    def get_user_table(self):
        return server.get_user_table()['str']

    def get_tables(self):
        return server.get_tables()['table.list']

    def quit(self):
        self.stop_threads = True
        server.leave_table()
        return server.quit()


instance = PykerProxy()
