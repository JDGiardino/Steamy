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


def get_rarest_achivement(game_id: int) -> dict :
    response = RequestsRetryClient().request(method='GET', url=f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
    loaded_json = json.loads(response.text)
    json_achivement_list = loaded_json["achievementpercentages"]["achievements"]
    rarest_achivement = min(x["percent"] for x in json_achivement_list)
    for x in json_achivement_list:
        if x["percent"] == rarest_achivement:
            return x