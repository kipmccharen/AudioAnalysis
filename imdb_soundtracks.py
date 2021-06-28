import requests
from dotenv import load_dotenv
import os 
from pprint import pprint
import json
import pandas as pd
from tmdbv3api import Movie, TMDb as tmdb
import time
from bs4 import BeautifulSoup

thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\" 
os.chdir(thisdir)
#load hidden credentials and values
load_dotenv() 
imdbapi_key = os.getenv("tmdbapikey")
master_list = pd.read_csv("tmdb_ids.csv", encoding='latin1')

imdb_id_list = master_list.imdb_id.tolist()
titles = master_list.title.tolist()

accum = []
# for ttid in imdb_id_list:
ttid = "tt0035423"
try:
    thisurl = f"https://www.imdb.com/title/{ttid}/soundtrack"
    page = requests.get(thisurl).text
    soup = BeautifulSoup(page, "html.parser")
    stdiv = soup.find('div' , id="soundtracks_content").div #grab table needed
    for c in stdiv.find_all("div"):
        strs = list(c.stripped_strings)
        accum.append([ttid] + strs)
except:
    pass
pprint(accum)