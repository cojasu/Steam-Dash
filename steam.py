import os
import random
import requests

STEAM_API_KEY = ""
STEAM_ID = ""
STEAM_API_URL = "https://api.steampowered.com/"
PLAYTIME_LIMIT = 10

def get_owned_games(api_key=STEAM_API_KEY, sid=STEAM_ID):
    game_list = []
    params = {'key': api_key, 'steamid': sid, 'format': 'json'}
    r = requests.get("{0}{1}".format(STEAM_API_URL, "IPlayerService/GetOwnedGames/v0001/"), params=params)
    for obj in r.json()['response']['games']:
        if PLAYTIME_LIMIT != None:
            if obj['playtime_forever'] <= PLAYTIME_LIMIT:
                game_list.append(obj)
        else:
            game_list.append(obj)
    return game_list

def get_random_game(game_list=get_owned_games()):
    return random.choice(game_list)

def launch_game(appid):
    command = "explorer steam://run/{0}".format(appid)
    os.system(command)

def run():
    launch_game(get_random_game()['appid'])