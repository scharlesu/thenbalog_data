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


def refactor_status(status_str):
  refactored = re.sub("\n                    ","",status_str)
  refactored = re.sub("                 ","",refactored)
  return refactored


def make_json(tables):
  out = []
  d2d = []
  for table in tables:
      names = table.findAll("span", attrs={"class":"CellPlayerName--long"})
      statuses = table.findAll("td", attrs={"style":" min-width: 200px; width: 40%;"})
      for (name, status) in zip(names, statuses):
        if("out" not in refactor_status(status.text).lower()):
           d2d.append(name.text)
        else:
           out.append(name.text)
        
  return {"out":out,"d2d":d2d}


#Add verification for if the json has changed and when it has then update json file, else don't update
#while 1:
with open("./thenbalog/_data/out_or_d2d.json","w") as outfile:
    json.dump(make_json(get_URL_data()),outfile)
print("out_or_d2d.json updated @ "+time.strftime("%H:%M:%S", time.localtime()))
  #time.sleep(60)
  