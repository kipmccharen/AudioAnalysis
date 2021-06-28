import urllib
from dotenv import load_dotenv
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import os 
import base64
import json

#Selenium items
from selenium import webdriver #webdriver to control activities
from selenium.webdriver.common.by import By #types of navigation
from selenium.webdriver.support.ui import WebDriverWait #waiting
import time

def start_driver(runheadless = False):
    """Initialize a Chrome webdriver with which for Selenium to act. """
    #set Chromedriver options to work smoothly
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized") # open Browser in maximized mode
    options.add_argument("disable-infobars") # disabling infobars
    options.add_argument("--disable-extensions") # disabling extensions
    options.add_argument("--disable-gpu") # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
    options.add_argument("--no-sandbox") # Bypass OS security model  
    if runheadless:
        options.add_argument("--headless")  
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(options=options,
            executable_path=r"D:\chromedriver.exe")
    driver.implicitly_wait(10) # seconds
    
    driver.get("https://www.google.com/") #open the given URL
    time.sleep(1) #wait for everything to load

    return driver

load_dotenv()

thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\" 
os.chdir(thisdir)

albumlist = pd.read_csv(r"allmusic_search_validated.csv")
hrefs = albumlist.to_dict('records')
#hrefs[:3]

driver = start_driver()

#for h in hrefs 
h = hrefs[0]

driver.get(h['am_href'])
time.sleep(1)

content = driver.page_source   

#content = requests.get(h['am_href']).text
soup = BeautifulSoup(content, "html.parser")
side = soup.find("section", attrs={'class':'basic-info'})

#sec1 = side.find_all("div")
lastone = None
#s = sec1[5]
#set(sub_list).issubset(set(test_list))
for s in side.find_all("div"):
    ss = list(s.stripped_strings)
    if ss:
        if lastone:
            if not set(ss).issubset(set(lastone)):
                h[ss[0]] = ss[1:]
        else:
            h[ss[0]] = ss[1:]
    lastone = ss.copy()

moods = soup.find("section", attrs={'class':'moods'})
if moods:
    h["moods"] = list(moods.div.stripped_strings)

themes = soup.find("section", attrs={'class':'moods'})
if themes:
    h["themes"] = list(themes.div.stripped_strings)

ratings = soup.find("ul", class_="ratings")
h['ratings'] = list(ratings.stripped_strings)

print(h)

driver.quit()