import pandas as pd 
from bs4 import BeautifulSoup
import requests
import os 
from pprint import pprint 

thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\" 
os.chdir(thisdir)

tlinks = pd.read_csv("trailer_links.csv", encoding='latin1')
tlinks = tlinks.query("getme == 'x'")
hrefs = tlinks.link.tolist()

baseurl = r"https://www.traileraddict.com"

trailist = []
print(len(hrefs))

for i, h in enumerate(hrefs):
    print(i,h)
    # h = r"/tremors/trailer"
    # i = 0
    page = requests.get(baseurl + h).text
    soup = BeautifulSoup(page, "html.parser")

    me = {'link': h, 'enum': i}

    txts = soup.find('div', id='interior')

    me['tags'] = '|'.join(list(txts.ul.stripped_strings))

    for s in txts.select('ul'):
        s.extract()

    heads = ["Duration", "Views", "Posted On", "Cast", 
        "Director", "Writer", "Studio", "Release", "Trailer Tracks"]

    strs = list(txts.stripped_strings)

    curr_hd = ""
    curr_list = []

    for x in strs:
        if x in heads:
            if curr_hd != "":
                me[curr_hd] = ';'.join(curr_list)
            curr_hd = x
            curr_list = []
        else:
            curr_list.append(x)
        #pprint(curr_hd)
        #pprint(curr_list)
    me[curr_hd] = ';'.join(curr_list)

    trailist.append(me)

df_trailers = pd.DataFrame(trailist)
df_trailers.shape
df_trailers.to_csv("trailer_details.csv")