from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import json
import re
import time
import os

load_dotenv()

url = os.getenv("INJURY_URL")

print(f"URL: {url}")

def get_URL_data():
  page_to_scrape = requests.get(url)
  soup = BeautifulSoup(page_to_scrape.text, "html.parser")
  tables = soup.findAll("div", attrs={"class":"TableBase"})
  return tables

def refactor_date(date_str):
  refactored = re.sub("\n                    \n    ","",date_str)
  refactored = re.sub("\n        ","",refactored)
  return refactored

def refactor_injury(injury_str):
  refactored = re.sub("\n                    ","",injury_str)
  refactored = re.sub("                 ","",refactored)
  return refactored

def refactor_status(status_str):
  refactored = re.sub("\n                    ","",status_str)
  refactored = re.sub("                 ","",refactored)
  return refactored

def make_list_players(table):
  list_players = []
  names = table.findAll("span", attrs={"class":"CellPlayerName--long"})
  dates = table.findAll("span", attrs={"class":"CellGameDate"})
  injuries = table.findAll("td", attrs={"style":" width: 20%;"})
  statuses = table.findAll("td", attrs={"style":" min-width: 200px; width: 40%;"})
  for (name, date, injury, status) in zip(names, dates, injuries, statuses):
    list_players.append({"name": name.text, "date": refactor_date(date.text), "injury": refactor_injury(injury.text), "status": refactor_status(status.text)})
  return list_players

def make_json(tables):
  json_obj = {"header": "NBA Injuries","teams": []}

  for table in tables:
    team_name = table.find("span", attrs={"class":"TeamName"})
    json_obj["teams"].append({"team_name": team_name.text, "players": ""})

  for(list_player, table) in zip(json_obj["teams"],tables):
    list_player["players"] = make_list_players(table)

  return json_obj


#Add verification for if the json has changed and when it has then update json file, else don't update
while 1:
  with open("../thenbalog/_data/injuries.json","w") as outfile:
      json.dump(make_json(get_URL_data()),outfile)
  print("injuries.json updated @ "+time.strftime("%H:%M:%S", time.localtime()))
  time.sleep(5)
  