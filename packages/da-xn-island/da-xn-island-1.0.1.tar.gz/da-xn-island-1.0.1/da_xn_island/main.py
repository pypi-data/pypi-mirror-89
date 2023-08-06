import requests
import random

BASE_URL = "https://island.da-xn.com/api.php"

def get_user(userID):
    if (userID == None or type(userID) != int):
        print("[Error]: Please specify a user id. If you want to view all users use the get_all_users() function.")
    else:
        r = requests.get(BASE_URL, params={"query": "getUser", "userID": userID})
        print(r.status_code)

def get_all_users():
    r = requests.get(BASE_URL, params={"query": "getUser"})
    print(r.status_code)

# Soon - def get_random_user():

def websiteStatus():
    r = requests.get("https://da-xn.com/statusApi.php")
    if (r.status_code == 200):
        r_dict = r.json()
        return r_dict["host_2"]
    else:
        return "Offline"

websiteStatus()
