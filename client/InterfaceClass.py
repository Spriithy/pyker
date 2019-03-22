from uuid import uuid4
import os
import http
import time
import requests
import json
from ApiCalls import instance_Server as api

def clear():
    os.system("clear")
class Interface():

    def __init__(self):
        print("")

    @staticmethod
    def print_Connexion():
        print("**** Connexion ****")
        return input("ID : ")

    @staticmethod
    def standard_Print(message,cleared=None, whoAmI=None):
        (clear()) if cleared!=None else ""
        (Interface.print_Clear_WhoAmI(whoAmI)) if whoAmI!=None else ""
        print("\n\n*********************************\n\n")
        print(message)
        print("\n\n*********************************\n\n")

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
    def set_Addr_Serv():
        address = input("Entrez l'adresse du serveur : ")
        try :
            ((api.set_addr_Serv(address))["status"]=="OK")
            print("Connexion établie avec le serveur")
            return True
        except :
            print("Server not found")
            return False

    @staticmethod
    def print_Creation():
        print()
    
