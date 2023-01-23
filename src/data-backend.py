# -*- coding: utf-8 -*-
"""FinalApp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B4wdVNDaJBKIv9zy6e6p_GrH__3n3ncJ
"""

! pip install pymongo[srv]
! pip install flask_cors
! pip install flask_ngrok

#Flask for app
from flask import Flask, request, jsonify, redirect
from flask_ngrok import run_with_ngrok
from flask_cors import CORS, cross_origin

import pymongo
from bson.json_util import ObjectId
import json

import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app, support_credentials=True)
run_with_ngrok(app)
client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

@app.route('/getplayerstats')
def get_playerstats():
  name = request.args.get('name') 
  # player = client.nba_stats.players.find_one({'PLAYER_NAME': name})
  # player.pop('_id')
  player = [row for row in client.nba_stats.games_details.find({'PLAYER_NAME': name})]
  playerinfo = pd.DataFrame.from_dict(player)

  try:
    playerinfo['MIN'] = playerinfo['MIN'].str.split(':', expand=True).astype(float)
    data = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK','MIN']].sum()
    games = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK']].count()
    data = data[data['MIN'] > 60]
    players_stat = pd.DataFrame(columns=[])
    players_stat['PLAYER_NAME'] = data['PLAYER_NAME']
    players_stat['FG'] = data['FGM']/data['FGA']*100
    players_stat['FT'] = data['FTM']/data['FTA']*100
    players_stat['REB_PER_GAME'] = (data['REB']/games['REB'])
    players_stat['AST_PER_GAME'] = (data['AST']/games['AST'])
    players_stat['BLK_PER_GAME'] = (data['BLK']/games['BLK'])
    players_stat['STL_PER_GAME'] = (data['STL']/games['STL'])

    players_stat.replace([np.inf, -np.inf], np.nan,inplace=True)
    players_stat = players_stat.fillna(0)
    players_stat['Overall'] = (((players_stat['FG']/100)*3) + ((players_stat['FT']/100)*2) + ((players_stat['REB_PER_GAME']/players_stat['REB_PER_GAME'].max())*1.5) + ((players_stat['AST_PER_GAME']/players_stat['AST_PER_GAME'].max())*1.5) + ((players_stat['BLK_PER_GAME']/players_stat['BLK_PER_GAME'].max())*1) + ((players_stat['STL_PER_GAME']/players_stat['STL_PER_GAME'].max())*1))/10 * 100
    # players_stat['Overall'] = players_stat['Overall']/players_stat['Overall'].max() *100
    # players_stat['Overall'] = players_stat['Overall'].round(decimals=1)
    players_stat = players_stat.round(decimals=1)

  except KeyError:
    return jsonify('Player not found')

  players_stat = players_stat.to_dict('records')
  return jsonify(players_stat)
  

@app.route('/insertfav') 
def insert_fav():
  name = request.args.get('name')
  check = [row for row in client.nba_stats.favplayers.find({'PLAYER_NAME': name})]
  ticket = True

  for i in check:
    if name == i['PLAYER_NAME']:
      ticket = False
  
  if ticket == True:
    player = [row for row in client.nba_stats.games_details.find({'PLAYER_NAME': name})]
    playerinfo = pd.DataFrame.from_dict(player)

    playerinfo['MIN'] = playerinfo['MIN'].str.split(':', expand=True).astype(float)
    data = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK','MIN']].sum()
    games = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK']].count()
    data = data[data['MIN'] > 60]
    players_stat = pd.DataFrame(columns=[])
    players_stat['PLAYER_NAME'] = data['PLAYER_NAME']
    players_stat['FG'] = data['FGM']/data['FGA']*100
    players_stat['FT'] = data['FTM']/data['FTA']*100
    players_stat['REB_PER_GAME'] = (data['REB']/games['REB'])
    players_stat['AST_PER_GAME'] = (data['AST']/games['AST'])
    players_stat['BLK_PER_GAME'] = (data['BLK']/games['BLK'])
    players_stat['STL_PER_GAME'] = (data['STL']/games['STL'])

    players_stat.replace([np.inf, -np.inf], np.nan,inplace=True)
    players_stat = players_stat.fillna(0)
    players_stat['Overall'] = (((players_stat['FG']/100)*3) + ((players_stat['FT']/100)*2) + ((players_stat['REB_PER_GAME']/players_stat['REB_PER_GAME'].max())*1.5) + ((players_stat['AST_PER_GAME']/players_stat['AST_PER_GAME'].max())*1.5) + ((players_stat['BLK_PER_GAME']/players_stat['BLK_PER_GAME'].max())*1) + ((players_stat['STL_PER_GAME']/players_stat['STL_PER_GAME'].max())*1))/10 * 100
    players_stat = players_stat.round(decimals=1)

    client.nba_stats.favplayers.insert(players_stat.to_dict('records'))

    res = players_stat.to_dict('records')

    return jsonify(res)
  else:
    res = [{'message':'Player already in list'}]
    return jsonify(res)

@app.route('/favremove')
def fav_remove():
  client.nba_stats.favplayers.remove()
  res = [{"message":'Removed'}]
  return jsonify(res)

@app.route('/fetchfav')
def fetch_fav():
  favs = [row for row in client.nba_stats.favplayers.find()]
  for i in favs:
    i.pop('_id')
  ret = dict()
  ret['data'] = favs
  return jsonify(ret)


@app.route('/listplayer')
def list_player():
  yr = request.args.get('year')
  yr = int(yr)
  plist = [row for row in client.nba_stats.players.find({'SEASON':yr})]
  players = []
  playersTemp = []
  for i in plist:
    players.append(i['PLAYER_NAME'])

  ret = dict()
  res = list(set(players))
  res.sort()

  for i in res:
    nm = dict()
    nm['name'] = i
    playersTemp.append(nm)

  ret['data'] = playersTemp
  return jsonify(ret)

@app.route('/getranks')
def get_ranks():
  rnge = request.args.get('range')
  rnge = int(rnge)
  store = [];
  rank = [row for row in client.nba_stats.ranking.find()]
  for i in rank:
    if rnge <= i['index'] <= rnge +9:
      i.pop('_id')
      store.append(i)
  res=dict()
  res['data'] = store

  return jsonify(res)

app.run()

# /getplayerstats?name=Kyrie%20Irving
# /listplayer?year=2019
# /insertfav?name=Kyrie Irving
# /favremove
# /getranks?range=5

"""## Send file to mongo"""

! gdown https://drive.google.com/uc?id=1v6OrkkX0kDhKdgtH7KONabaWaccnFSZp
! gdown https://drive.google.com/uc?id=1Z4cvkBBY7hEpQ_LPhv93ke0OTh9xC3Jb
! gdown https://drive.google.com/uc?id=1vtgX6RWCcN0kBqCczHqRCf6PNNI9RrNY
! gdown https://drive.google.com/uc?id=1GKIqv9xnkb9OgkljAUcxkbU-RmRji4zF
! gdown https://drive.google.com/uc?id=1hn0oYQsJm4N8k4MlMvRMnzizKtNKp9Hb

#import data to mongoDB
import pandas as pd
import pymongo
from bson.json_util import ObjectId
import json

client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.nba_stats
data = pd.read_csv('games.csv')
data1 = pd.read_csv('games_details.csv')
data2 = pd.read_csv('players.csv')
data3 = pd.read_csv('ranking.csv')
data4 = pd.read_csv('teams.csv')
db.games.insert_many(data.to_dict('records'))
db.games_details.insert_many(data1.to_dict('records'))
db.players.insert_many(data2.to_dict('records'))
db.ranking.insert_many(data3.to_dict('records'))
db.teams.insert_many(data4.to_dict('records'))

"""# Try Codes #"""

import pymongo
import pandas as pd
import numpy as np

client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

year = 2015
plist = [row for row in client.nba_stats.players.find({'SEASON':year})]
players = []
for i in plist:
  players.append(i['PLAYER_NAME'])
res = set(players)
type(res)
res

import pymongo
import pandas as pd
import numpy as np

client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

name = 'AJ Price'

player = [row for row in client.nba_stats.games_details.find({'PLAYER_NAME': name})]
playerinfo = pd.DataFrame.from_dict(player)

try:
  playerinfo['MIN'] = playerinfo['MIN'].str.split(':', expand=True).astype(float)
  data = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK','MIN']].sum()
  games = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK']].count()
  data = data[data['MIN'] > 60]
  players_stat = pd.DataFrame(columns=[])
  players_stat['PLAYER_NAME'] = data['PLAYER_NAME']
  players_stat['FG%'] = data['FGM']/data['FGA']*100
  players_stat['FT%'] = data['FTM']/data['FTA']*100
  players_stat['REB_PER_GAME'] = (data['REB']/games['REB'])
  players_stat['AST_PER_GAME'] = (data['AST']/games['AST'])
  players_stat['BLK_PER_GAME'] = (data['BLK']/games['BLK'])
  players_stat['STL_PER_GAME'] = (data['STL']/games['STL'])

  players_stat.replace([np.inf, -np.inf], np.nan,inplace=True)
  players_stat = players_stat.fillna(0)
  players_stat['Overall'] = (((players_stat['FG%']/100)*3) + ((players_stat['FT%']/100)*2) + ((players_stat['REB_PER_GAME']/players_stat['REB_PER_GAME'].max())*1.5) + ((players_stat['AST_PER_GAME']/players_stat['AST_PER_GAME'].max())*1.5) + ((players_stat['BLK_PER_GAME']/players_stat['BLK_PER_GAME'].max())*1) + ((players_stat['STL_PER_GAME']/players_stat['STL_PER_GAME'].max())*1))/10 * 100
  # players_stat['Overall'] = players_stat['Overall']/players_stat['Overall'].max() *100
  players_stat['Overall'] = players_stat['Overall'].round(decimals=1)

except KeyError:
  print('Player not found')

players_stat = players_stat.to_dict('records')
players_stat

import pymongo
import pandas as pd
import numpy as np
client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

name = 'Kyrie Irving'
check = [row for row in client.nba_stats.favplayers.find({'PLAYER_NAME': name})]
ticket = True

for i in check:
  if name == i['PLAYER_NAME']:
    ticket = False
    print('in')

# run here in true
if ticket == True:
  print('true')




if ticket == False:
  print('false')

import pymongo
import pandas as pd
import numpy as np
client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

yo = [row for row in client.nba_stats.favplayers.find()]
for i in yo:
    i.pop('_id')
yo

import pymongo
import pandas as pd
import numpy as np
client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
player = [row for row in client.nba_stats.games_details.find()]
playerinfo = pd.DataFrame.from_dict(player)

playerinfo

playerinfo['MIN'] = playerinfo['MIN'].str.split(':', expand=True).astype(float)
data = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK','MIN']].sum()
games = playerinfo.groupby(['PLAYER_NAME'],as_index=False)[['FTA','FTM','FGA','FGM','REB','AST','STL','BLK']].count()
data = data[data['MIN'] > 60]
players_stat = pd.DataFrame(columns=[])
players_stat['PLAYER_NAME'] = data['PLAYER_NAME']
players_stat['FG'] = data['FGM']/data['FGA']*100
players_stat['FT'] = data['FTM']/data['FTA']*100
players_stat['REB_PER_GAME'] = (data['REB']/games['REB'])
players_stat['AST_PER_GAME'] = (data['AST']/games['AST'])
players_stat['BLK_PER_GAME'] = (data['BLK']/games['BLK'])
players_stat['STL_PER_GAME'] = (data['STL']/games['STL'])

players_stat.replace([np.inf, -np.inf], np.nan,inplace=True)
players_stat = players_stat.fillna(0)
players_stat['Overall'] = (((players_stat['FG']/100)*3) + ((players_stat['FT']/100)*2) + ((players_stat['REB_PER_GAME']/players_stat['REB_PER_GAME'].max())*1.5) + ((players_stat['AST_PER_GAME']/players_stat['AST_PER_GAME'].max())*1.5) + ((players_stat['BLK_PER_GAME']/players_stat['BLK_PER_GAME'].max())*1) + ((players_stat['STL_PER_GAME']/players_stat['STL_PER_GAME'].max())*1))/10 * 100
players_stat['Overall'] = players_stat['Overall']/players_stat['Overall'].max() *100
players_stat['Overall'] = players_stat['Overall'].round(decimals=1)
players_stat = players_stat.round(decimals=1)

players_stat

sorted = players_stat.sort_values(['FG','PLAYER_NAME'],ascending=False)
ratings = sorted.reset_index(drop = True)
ratings.index = ratings.index + 1
ratings = ratings.reset_index()
ratings

import pandas as pd
import pymongo
from bson.json_util import ObjectId
import json

client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


client.nba_stats.ranking.insert_many(ratings.to_dict('records'))

import pymongo
import pandas as pd
import numpy as np
client = pymongo.MongoClient("mongodb+srv://ise2190101User:7Xck5PyPEOAjG44K@cluster0.7c8oq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

range = 10;
store = [];
rank = [row for row in client.nba_stats.ranking.find()]
rank
# for i in rank:
#   if range <= i['index'] <= range +10:
#     i.pop('_id')
#     store.append(i)
# store

for i in range(-1, 5):
    print(i, end=", ")