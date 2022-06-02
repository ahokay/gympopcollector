import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import sys
import csv
import time

data =  {"username": sys.argv[1], "password": sys.argv[2], "button": "login", "__RequestverificationToken": ""}
data2 = {"code": "", "id_token": "", "scope": "", "state": "", "session_state": ""}
headers = ["Date Time", "Population"]

def login():
    with requests.session() as session:
        r = session.get("https://puregym.com/members/")
        rsoup = bs(r.text, "html.parser")
        token = rsoup.find("input", {"name": "__RequestVerificationToken"})
        data["__RequestverificationToken"] = token["value"]
        r = session.post(r.url, data=data)
        rsoup = bs(r.text, "html.parser")
        code = rsoup.find("input", {"name": "code"})["value"]
        id_token = rsoup.find("input", {"name": "id_token"})["value"]
        scope = rsoup.find("input", {"name": "scope"})["value"]
        state = rsoup.find("input", {"name": "state"})["value"]
        session_state = rsoup.find("input", {"name": "session_state"})["value"]
        data2["code"] = code
        data2["id_token"] = id_token
        data2["scope"] = scope
        data2["state"] = state
        data2["session_state"] = session_state
        r = session.post("https://idclient.puregym.com/signin-oidc", data=data2)
        return r


def getNumberOfPeople():
    rsoup = bs(login().text, "html.parser").find("p", {"id": "people_in_gym"}).text
    number = ""
    for i in rsoup:
        try:
            int(i)
            number += i
        except ValueError:
            continue
    return number


def saveNumber():
    numberOfPeople = getNumberOfPeople()
    with open("gympopulation.csv", "a") as file:
        dictfile = csv.DictWriter(file, fieldnames=headers)
        currenttime = datetime.now()
        currenttime = datetime.strftime(currenttime, "%d/%m/%Y %H:%M")
        data = {}
        data["Date Time"] = currenttime
        data["Population"] = numberOfPeople
        dictfile.writerow(data)


def checkFile():
    try:
        with open("gympopulation.csv") as file:
            pass
    except Exception:
        with open("gympopulation.csv", "w") as file:
            dictfile = csv.DictWriter(file, fieldnames=headers)
            dictfile.writeheader()


def operator():
    while True:
        checkFile()
        saveNumber()
        time.sleep(15*60)


if __name__ == "__main__":
    operator()
