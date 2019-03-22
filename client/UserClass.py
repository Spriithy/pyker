from ApiCalls import instance_Server as api

class UserClass():
    def __init__(self):
        self.IDs_=None
        self.last_Message=0

    def whoAmI(self):
        return self.IDs_
    
    def pull_Message(self):
        messages_Pulled=api.pull_Messages(self.last_Message)
        self.last_Message=self.last_Message+len(messages_Pulled["lobby.messages"])
        return messages_Pulled["lobby.messages"]

    def push_Message(self,message,to='lobby') :
        if(len(message.strip())==0):
            return False
        return True if (api.push_Message(message,to)["status"]=="OK") else False

    def ping_Serv(self):
        api.ping_Serv()
user = UserClass()