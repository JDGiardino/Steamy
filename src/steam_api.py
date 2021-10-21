import steam
import gevent.monkey
import requests
import json
import os
from src.utils.requests_retry_client import RequestsRetryClient
from steam.steamid import SteamID

STEAM_API_KEY = os.environ.get('STEAM_API_KEY') #Obtain a Steam Web API Key from https://steamcommunity.com/dev/apikey
if not STEAM_API_KEY:
    raise Exception('No STEAM_API_KEY provided')


def get_steam_id(community_name: str) -> int:
    return steam.steamid.from_url(f'https://steamcommunity.com/id/{community_name}') #This takes a Steam community URL for a profile and converts it to a SteamID


def get_game_id(game: str) -> int:
    response = RequestsRetryClient().request(method='GET', url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    json_app_list = json.loads(response.text)  #Load the JSON data into a list of dictionaries
    for x in json_app_list["applist"]["apps"]:
        if game == x['name']:
            return x['appid']


def get_rarest_achievement(game_id: int) -> dict:
    response = RequestsRetryClient().request(method='GET', url=f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
    loaded_json = json.loads(response.text)  #Load the JSON data into a list of dictionaries
    json_achievement_list = loaded_json["achievementpercentages"]["achievements"]
    rarest_achievement = min(x["percent"] for x in json_achievement_list)
    for x in json_achievement_list:
        if x["percent"] == rarest_achievement:
            return x


def get_users_game_playtime(user_id: int, game_id: int) -> dict:
    response = RequestsRetryClient().request(method='GET', url=f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={user_id}&format=json")
    loaded_json = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    playtimes = loaded_json["response"].get("games")
    if playtimes is None:
        return None #This catches if the json object does not have the assumed nested items
    else:
        for x in playtimes:
            if x["appid"] == game_id:
                return x


def get_users_total_playtime(user_id: int) -> float:
    response = RequestsRetryClient().request(method='GET', url=f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={user_id}&format=json")
    loaded_json = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    playtimes = loaded_json["response"].get("games")
    if playtimes is None:
        return None #This catches if the json object does not have the assumed nested items
    else:
        total_playtime = 0
        for x in playtimes:
            total_playtime += x["playtime_forever"]
        return total_playtime

