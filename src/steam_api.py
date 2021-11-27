import steam
import json
import os

from typing import Union
from src.models.AchievementPercent import AchievementPercent
from src.models.AchievementDetails import AchievementDetails
from src.models.PlayerAchievements import PlayerAchievements
from src.models.Game import Game
from src.models.Players import Players
from src.models.Playtime import Playtime
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


def get_game(game_name: str) -> Game:
    response = RequestsRetryClient().request(method='GET',
                                             url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    json_app_list = json.loads(response.text)  # Load the JSON data into a list of dictionaries
    for x in json_app_list["applist"]["apps"]:
        if game_name == x['name']:
            return Game(**x)


def get_achievement_percent(game_id: int) -> AchievementPercent:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
    loaded_json = json.loads(response.text)
    json_achievement_list = loaded_json["achievementpercentages"]["achievements"]
    rarest_achievement = min(x["percent"] for x in json_achievement_list)
    for x in json_achievement_list:
        if x["percent"] == rarest_achievement:
            return AchievementPercent(**x)


def get_achievement_details(achievement_name: str, game_id: int) -> AchievementDetails:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={STEAM_API_KEY}&appid={game_id}")
    loaded_json = json.loads(response.text)
    json_achievements = loaded_json["game"]["availableGameStats"]["achievements"]
    for x in json_achievements:
        if x["name"] == achievement_name:
            return AchievementDetails(**x)


def get_game_playtimes(user_id: int, game_id: int) -> Union[None, Playtime]:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={user_id}&format=json")
    loaded_json = json.loads(response.text)
    playtime = loaded_json["response"].get("games")
    if playtime is None:
        return None  # This catches if the json object does not have the assumed nested items
    else:
        for x in playtime:
            if x["appid"] == game_id:
                return Playtime(**x)


def get_game_icon(game_id: int) -> str:
    return f"https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/header.jpg"


def get_player_achievements(user_id: int, game_id: int) -> PlayerAchievements:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={STEAM_API_KEY}&appid={game_id}&steamid={user_id}")
    loaded_json = json.loads(response.text)
    achievements = loaded_json["playerstats"]["achievements"]
    unlocked = 0
    total = 0
    for x in achievements:
        if x["achieved"] == 1:
            unlocked += 1
        total += 1
    return PlayerAchievements(unlocked=unlocked, total=total,)


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


def get_players(game_id: int) -> Players:
    response = RequestsRetryClient().request(method='GET',
                                             url=f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid={game_id}")
    loaded_json = json.loads(response.text)
    x = loaded_json["response"]
    return Players(**x)


def get_all_game_player_counts():
    all_games = get_all_games()
    for x in all_games:
        response = RequestsRetryClient().request(method='GET',  # can this take multiple app ids per API call?  print statements to see how long it takes, maybe hitting errors?  How many requests allowed?  Keep researching better top games APIs to hit.
                                                 url=f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid={x['appid']}")
        loaded_json = json.loads(response.text)
        player_count = loaded_json["response"]
        x.update(player_count)
    return all_games

