import steam
import json
import os

from typing import Union
from Achievement import Achievement
from Game import Game
from Players import Players
from Playtime import Playtime
from src.utils.requests_retry_client import RequestsRetryClient
from steam.steamid import SteamID

STEAM_API_KEY = os.environ.get('STEAM_API_KEY')  # Obtain a Steam Web API Key from https://steamcommunity.com/dev/apikey
if not STEAM_API_KEY:
    raise Exception('No STEAM_API_KEY provided')


def get_all_games() -> dict:
    response = RequestsRetryClient().request(method='GET',
                                             url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    json_app_list = json.loads(response.text)
    return json_app_list["applist"]["apps"]


def get_steam_id(community_name: str) -> int:
    return steam.steamid.from_url(f'https://steamcommunity.com/id/{community_name}')
    # This takes a Steam community URL for a profile and converts it to a SteamID


def get_game_id(game_name: str) -> Game:
    response = RequestsRetryClient().request(method='GET',
                                             url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    json_app_list = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    for x in json_app_list["applist"]["apps"]:
        if game_name == x['name']:
            return Game(**x)
            # Nothing outside of steam_api.py should be interacting with raw dicts, therefore we return data classes


def get_rarest_achievement(game_id: int) -> Achievement:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
    loaded_json = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    json_achievement_list = loaded_json["achievementpercentages"]["achievements"]
    rarest_achievement = min(x["percent"] for x in json_achievement_list)
    for x in json_achievement_list:
        if x["percent"] == rarest_achievement:
            return Achievement(**x)


def get_users_game_playtime(user_id: int, game_id: int) -> Union[None, Playtime]:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={user_id}&format=json")
    loaded_json = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    playtime = loaded_json["response"].get("games")
    if playtime is None:
        return None  # This catches if the json object does not have the assumed nested items
    else:
        for x in playtime:
            if x["appid"] == game_id:
                return Playtime(**x)


def get_users_total_playtime(user_id: int) -> Union[None, float]:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={user_id}&format=json")
    loaded_json = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    playtime = loaded_json["response"].get("games")
    if playtime is None:
        return None  # This catches if the json object does not have the assumed nested items
    else:
        total_playtime = 0
        for x in playtime:
            total_playtime += x["playtime_forever"]
        return total_playtime


def get_game_player_count(game_id: int) -> Players:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid={game_id}")
    loaded_json = json.loads(response.text)
    x = loaded_json["response"]
    return Players(**x)


def get_all_game_player_counts():
    all_games = get_all_games()
    for x in all_games:
        response = RequestsRetryClient().request(method='GET',
                                                 url=f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid={x['appid']}")
        loaded_json = json.loads(response.text)
        player_count = loaded_json["response"]
        x.update(player_count)
    return all_games

