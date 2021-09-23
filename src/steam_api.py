import steam
import gevent.monkey
gevent.monkey.patch_all()
import requests
import json
from src.utils.requests_retry_client import RequestsRetryClient
from steam.steamid import SteamID

api_key = '7733C86DC8282F528C8DB110AF14185D' #Obtain a Steam Web API Key from https://steamcommunity.com/dev/apikey


def get_steam_id(community_name: str) -> int:
    return steam.steamid.from_url(f'https://steamcommunity.com/id/{community_name}') #This takes a Steam community URL for a profile and converts it to a SteamID


def get_game_id(game: str) -> int:
    response = RequestsRetryClient().request(method='GET', url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    json_app_list = json.loads(response.text)  #Load the JSON data into a list of dictionaries
    for x in json_app_list["applist"]["apps"]:
        if game == x['name']:
            return x['appid']


def get_rarest_achievement(game_id: int) -> dict :
    response = RequestsRetryClient().request(method='GET', url=f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
    loaded_json = json.loads(response.text)  #Load the JSON data into a list of dictionaries
    json_achievement_list = loaded_json["achievementpercentages"]["achievements"]
    rarest_achievement = min(x["percent"] for x in json_achievement_list)
    for x in json_achievement_list:
        if x["percent"] == rarest_achievement:
            return x


def get_users_playtime(user_id: int, game_id: int) -> dict:
    response = RequestsRetryClient().request(method='GET', url=f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={user_id}&format=json")
    loaded_json = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    playtimes = loaded_json["response"]["games"]
    for x in playtimes:
        if x["appid"] == game_id:
            return x