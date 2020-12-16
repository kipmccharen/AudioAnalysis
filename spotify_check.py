import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd
from pprint import pprint
import os 

thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\" 
os.chdir(thisdir)

load_dotenv()

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
current_uri = r"spotify:playlist:37i9dQZF1EM54Do0s21iBr"

scope = "user-library-read"
#auth_manager = SpotifyOAuth(scope=scope)

# sp = spotipy.Spotify(auth_manager=auth_manager)
# cats = sp.categories(country="US", limit=50)
# cats = cats['categories']
# cats = cats['items']
# catdf = pd.json_normalize(cats)
# catdf.to_csv("spotifycategories.csv")
# # results = sp.current_user_saved_tracks()
# # for idx, item in enumerate(results['items']):
# #     track = item['track']
# #     print(idx, track['artists'][0]['name'], " – ", track['name'])

playlistid = "37i9dQZF1EM54Do0s21iBr"
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

pl = sp.playlist_items(playlist_id=playlistid)


df = pd.json_normalize(pl['items'])
df.to_csv("playlist_norm.csv")
#print(df.head())
# playlists = sp.user_playlists('spotify')
# rightplaylist = [x for x in playlists['items'] if x['uri'] == current_uri]
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None