from uuid import uuid4
import os
import http
import time
import requests
import json
from ApiCalls import instance_Server as api
from UserClass import user as user

def clear():
    os.system("clear")

class Interface():

    def __init__(self):
        print("")

    @staticmethod
    def set_Addr_Serv():
        response=False
        while (response==False):
            address = input("Entrez l'adresse du serveur : ")
            username= input("Votre username : ")
            username = "Anonymous" if len(username)==0 else username 
            try :
                response = api.set_addr_Serv(address,username)
                print("Connexion établie avec le serveur")
                return response #ID
            except :
                print("Server not found")

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
        print("\n\n*********************************\n\n")
        print(message)
        print("\n\n*********************************\n\n")
    
