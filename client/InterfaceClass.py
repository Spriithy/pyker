from uuid import uuid4
import os
import http
import time
import requests
import json

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
    def print_Creation():
        print()
    
