import gevent.monkey
gevent.monkey.patch_all()
import requests
import json
from src.utils.requests_retry_client import RequestsRetryClient


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