from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import json
import re
import time
import os

load_dotenv()

url = os.getenv("PROFILE_URL")

print(f"URL: {url}")

def get_URL_data():
  page_to_scrape = requests.get(url)
  soup = BeautifulSoup(page_to_scrape.text, "html.parser")
  tables = soup.findAll("a", attrs={"class":"players-group__player"})
  print(''.join(filter(lambda i: i.isdigit(), tables[0].get("href"))))
  return tables


def make_json(tables):
  list_players = []
  for player in tables:
    name = player.text.split("\n\t\t\t\t\t\t\t")[1]
    name = name.split("\t\t\t\t\t\t")[0]
    name = name.split(" ")[1] + " " + name.split(" ")[0] 
    id=("".join(filter(lambda i: i.isdigit(), player.get("href"))))
    image= "https://www.dunkest.com/img/players/nba/" + id + ".png"
    list_players.append([
       {"name": name},
       {"image": image}
    ])
  return list_players



#Add verification for if the json has changed and when it has then update json file, else don't update
with open("./thenbalog/data/profiles.json","w") as outfile:
    json.dump(make_json(get_URL_data()),outfile)
print("profiles.json updated @ "+time.strftime("%H:%M:%S", time.localtime()))
  