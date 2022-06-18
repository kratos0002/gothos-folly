# Import libraries

from dataclasses import dataclass
from pprint import pprint
import pickle
import re
import requests
import urllib3.request
import urllib.parse
import json
import numpy as np
import pandas as pd
import random
from tqdm import tqdm
from bs4 import BeautifulSoup
#from sklearn.preprocessing import minmax_scale
#import nltk
#nltk.download('stopwords')
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
#from nltk.stem.wordnet import WordNetLemmatizer  # default lemmatizer
# Visualization
#import matplotlib.pyplot as plt
# plt.style.use('raph-base')
#import seaborn as sns



base = "https://api.genius.com"
genius_token = 'kUFoaITFV3dfWykZAeCYC79H7uHlnq6c-7j4qblwV_RJculHZCWrYKBdTbu41ND_'



def get_json(path, params=None, headers=None):
    '''Send request and get response in json format.'''

    # Generate request URL
    requrl = '/'.join([base, path])
    token = f"Bearer {genius_token}"
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}
    # Get response object from querying genius api
    response = requests.get(url=requrl, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def get_artist(name):
  search = "/search?q="
  query = base + search + urllib.parse.quote(name)+'&access_token='+genius_token
  response = requests.get(query)
  apod_str = json.dumps(response.json())
  apod_dict = json.loads(apod_str)
  # df_apod = pd.DataFrame(apod_dict)
  # print(apod_dict['response']['hits'])
  data = apod_dict['response']['hits']
  return data[0]['result']['primary_artist']['id']

artist = input('Which artist')
list_of_artists = [artist]
pick_artist = random.choice(list_of_artists)
id = get_artist(pick_artist)
print(pick_artist)


def get_songlist(artist_id):
  current_page = 1
  next_page = True
  songs = []
  while next_page:
    path = f"artists/{artist_id}/songs/"
    params = {'page': current_page} # the current page
    data = get_json(path=path, params=params) # get json of songs
    page_songs = data['response']['songs']
    if page_songs:
      songs +=page_songs
      current_page+=1
      print(f"Page {current_page} finished scraping")
    else:
      next_page = False
  print(f"Song id were scraped from {current_page} pages")

  songlist = {song['id']:song['title'].lower() for song in songs
              if song['primary_artist']['id']==artist_id}
  return songlist

list = get_songlist(id)

#print(list)

#list = {id:title for id,title in list.items() if "live" not in title}

#print(len(list))

def path_lyrics(song_id):
  path = f"songs/{song_id}"
  song = get_json(path)
  song_path = song['response']['song']['path']
  return song_path
def get_lyrics(song_id):
  path = path_lyrics(song_id)
  lyrics_url = "http://genius.com" + path
  lyrics_page = requests.get(lyrics_url)
  html = BeautifulSoup(lyrics_page.content, "html.parser")
  old_div = html.find("div", class_="lyrics")
  new_div = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 jYfhrf")
  if old_div:
    lyrics = old_div.get_text()
  elif new_div:
    lyrics = str(new_div)
    lyrics = lyrics.replace('<br/>', '\n')
    lyrics = re.sub(r'(\<.*?\>)', '', lyrics)
  else:
    return None


  # lyrics = html.find("div", class_ = "lyrics").get_text()
  return lyrics

def get_lyr_artist(songlist):
  lyrics_dict = {}
  for song_id, title in tqdm(songlist.items()):
    lyrics_dict[title] = get_lyrics(song_id)
  return lyrics_dict

def get_random_song_lyrics(songlist):
  x = [i for i in songlist.keys()]
  rand = random.choice(x)
  print(rand)
  song_name =  get_song_name(rand)
  print("Song Name: "+song_name)
  albumname = get_album_name(rand)
  print("Album Name: "+albumname)
  x_lyrics = get_lyrics(rand)
  print(x_lyrics)
  return x_lyrics


def get_all_lyrics(songlist):
    all_lyrics = []
    for song in songlist.keys():
        songmeta ={}
        songmeta['_id'] = song
        songmeta['name'] = get_song_name(song)
        songmeta['Album Name'] = get_album_name(song)
        inner_text = get_lyrics(song)
        if inner_text:
            inner_text = inner_text.replace('\\n','\n')
        else:
            inner_text = None
        # inner_text = [x.replace("\\n", "") for x in inner_text]
        # print(inner_text)
        # final_lyrics = "".join(inner_text[:-4])
        # print(inner_text)
        songmeta['lyrics']=inner_text 
        songmeta['artist']=pick_artist
        # print("songmeta")
        # print(songmeta)
        all_lyrics.append(songmeta)
        
    return all_lyrics
        
  


def get_song_name(song_id):
  path = f"songs/{song_id}"
  song = get_json(path)
  song_name = song['response']['song']['full_title']
  return song_name

def get_album_name(song_id):
  path = f"songs/{song_id}"
  song = get_json(path)
  try:
    album_name = song['response']['song']['album']['name']
    return album_name
  except:
    return None

print(pick_artist)
LZ = get_all_lyrics(list)
# print(LZ)
  
import pandas as pd
df = pd.DataFrame(LZ)

# importing module
from pymongo import MongoClient

# creation of MongoClient
client=MongoClient()

# Connect with the portnumber and host
client = MongoClient("mongodb://kratos0002:Mongodbsucks.123@ac-8w501ar-shard-00-00.u5ocxsz.mongodb.net:27017,ac-8w501ar-shard-00-01.u5ocxsz.mongodb.net:27017,ac-8w501ar-shard-00-02.u5ocxsz.mongodb.net:27017/?ssl=true&replicaSet=atlas-vu9haa-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.musicdb

records = db.music_c
dict = df.to_dict('records')

records.insert_many(dict)
print('all records moved to mongo')


