from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import json
import re
import time
import os

load_dotenv()

url = os.getenv("DEPTH_URL")

print(f"URL: {url}")
def name_formater(string):
  for i in range(10):
    string = string.replace(str(i),"")
  string = string.replace("\n\n#","")
  if(string == "\xa0"):
    return " "
  if(string == "Bruce Brown, Jr."):
    return "Bruce Brown"
  return string
def team_name_formater(string):
  return string.replace(' Depth Chart',"").replace('2024-2025' ,"").replace("\n ","").replace("\n","")

def get_URL_data():
  page_to_scrape = requests.get(url)
  soup = BeautifulSoup(page_to_scrape.text, "html.parser")
  tables = soup.findAll("table",attrs={"class":"basketball"})
  #print(tables)
  return tables

def get_URL_names():
  page_to_scrape = requests.get(url)
  soup = BeautifulSoup(page_to_scrape.text, "html.parser")
  names = soup.findAll("h2",attrs={"class":"clearfix"})
  return names

def make_json(tables, names):
  json_object = []
  team={}
  for table,name in zip(tables,names):
    pg = []
    sg = []
    sf = []
    pf = []
    c = []   
    team_name = team_name_formater(name.text)
    if("Los Angeles" in team_name):
      team_name = team_name.replace("Los Angeles","LA")
    if("Sixers" in team_name):
      team_name = team_name.replace("Sixers","76ers")
    rows = table.findAll("tr")[1:]
    for row in rows:
      pg.append(name_formater(row.findAll("td")[1].text))
      sg.append(name_formater(row.findAll("td")[2].text))
      sf.append(name_formater(row.findAll("td")[3].text))
      pf.append(name_formater(row.findAll("td")[4].text))
      c.append(name_formater(row.findAll("td")[5].text))
    
    team = {"team":team_name,"depth":{"pg":pg, "sg":sg,"sf":sf,"pf":pf,"c":c}}
    json_object.append(team)
  return json_object



#Add verification for if the json has changed and when it has then update json file, else don't update
with open("./thenbalog/_data/depth.json","w") as outfile:
    json.dump(make_json(get_URL_data(),get_URL_names()),outfile)
print("depth.json updated @ "+time.strftime("%H:%M:%S", time.localtime()))
  