import time
from sys import platform
import os

def wait(seconds):
    time.sleep(seconds)

def clear():
    if (platform == "linux" or platform == "linux2" or platform == "darwin"):
        os.system("clear")
    elif (platform == "win32" or platform == "win64"):
        os.system("cls")
    else:
        os.system("clear")
