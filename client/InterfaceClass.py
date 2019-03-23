import os
from ApiCalls import instance_Server as api
from UserClass import user as user

def clear():
    os.system("clear")

class InterfaceClass():

    def __init__(self):
        print("")

    @staticmethod
    def set_Addr_Serv(address):
        response=False
        while (response==False):
            username= input("Votre username : ")
            username = "Anonymous" if len(username)==0 else username 
            try :
                response = api.set_addr_Serv(address,username)
                print("Connexion établie avec le serveur")
                return response["user.name"],response["user.id"]
            except :
                print("Server not found")
                exit(0)

    @staticmethod
    def print_Clear_WhoAmI(name):
        clear()
        print("Connecté en tant que %s"%name)

    @staticmethod
    def print_Interface(username):
        Interface.standard_Print("Create or join table ?",whoAmI=username)
        choise=input(">")
        print(choise=="c")
        #if(choise=="c"):
            #print_Creation()
    
    @staticmethod
    def print_Creation():
        print()

    @staticmethod
    def standard_Print(message,cleared=None, whoAmI=None):
        (clear()) if cleared!=None else ""
        (Interface.print_Clear_WhoAmI(whoAmI)) if whoAmI!=None else ""
        print("\n*********************************\n")
        print(message)
        print("\n*********************************\n")
    
