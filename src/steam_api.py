import steam
import json
import os

from typing import Union
from src.models.AchievementPercent import AchievementPercent
from src.models.AchievementDetails import AchievementDetails
from src.models.PlayerAchievements import PlayerAchievements
from src.models.PlayerSummary import PlayerSummary
from src.models.Game import Game
from src.models.Players import Players
from src.models.Playtime import Playtime
from src.models.GameDetails import GameDetails
from src.utils.requests_retry_client import RequestsRetryClient
from steam.steamid import SteamID


class SteamApi(object):

    def __init__(self):
        self.STEAM_API_KEY = os.environ.get('STEAM_API_KEY')
        # Obtain a Steam Web API Key from https://steamcommunity.com/dev/apikey
        if not self.STEAM_API_KEY:
            raise Exception('No STEAM_API_KEY provided')

    def __request(self, url: str) -> dict:  # __ private function, no one outside this class needs t
        response = RequestsRetryClient().request(method='GET', url=url)
        return json.loads(response.text)

    def get_all_games(self) -> dict:
        json_app_list = self.__request("https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
        # TO DO  Repeat this for each method that it applied to ^^^
        return json_app_list["applist"]["apps"]

    def get_steam_id(self, community_name: str) -> int:
        return steam.steamid.from_url(f'https://steamcommunity.com/id/{community_name}')
        # This takes a Steam community URL for a profile and converts it to a SteamID

    def get_game(self, game_name: str) -> Game:
        json_app_list = self.__request("https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
        for x in json_app_list["applist"]["apps"]:
            if game_name == x['name']:
                return Game(**x)

    def get_achievement_percent(self, game_id: int) -> AchievementPercent:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
        json_achievement_list = loaded_json["achievementpercentages"]["achievements"]
        rarest_achievement = min(x["percent"] for x in json_achievement_list)
        for x in json_achievement_list:
            if x["percent"] == rarest_achievement:
                return AchievementPercent(**x)

    def get_achievement_details(self, achievement_name: str, game_id: int) -> AchievementDetails:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={self.STEAM_API_KEY}&appid={game_id}")
        json_achievements = loaded_json["game"]["availableGameStats"]["achievements"]
        for x in json_achievements:
            if x["name"] == achievement_name:
                return AchievementDetails(**x)

    def get_game_playtimes(self, user_id: int, game_id: int) -> Union[None, Playtime]:
        loaded_json = self.__request(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.STEAM_API_KEY}&steamid={user_id}&format=json")
        playtime = loaded_json["response"].get("games")
        if playtime is None:
            return None  # This catches if the json object does not have the assumed nested items
        else:
            for x in playtime:
                if x["appid"] == game_id:
                    return Playtime(**x)

    def get_game_icon(self, game_id: int) -> str:
        return f"https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/header.jpg"

    def get_player_achievements(self, user_id: int, game_id: int) -> PlayerAchievements:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={self.STEAM_API_KEY}&appid={game_id}&steamid={user_id}")
        achievements = loaded_json["playerstats"]["achievements"]
        unlocked = 0
        total = 0
        for x in achievements:
            if x["achieved"] == 1:
                unlocked += 1
            total += 1
        return PlayerAchievements(unlocked=unlocked, total=total,)

    def get_users_total_playtime(self, user_id: int) -> Union[None, float]:
        loaded_json = self.__request(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.STEAM_API_KEY}&steamid={user_id}&format=json")
        playtime = loaded_json["response"].get("games")
        if playtime is None:
            return None  # This catches if the json object does not have the assumed nested items
        else:
            total_playtime = 0
            for x in playtime:
                total_playtime += x["playtime_forever"]
            return total_playtime

    def get_player_summaries(self, user_id: int) -> PlayerSummary:
        loaded_json = self.__request(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.STEAM_API_KEY}&steamids={user_id}")
        return PlayerSummary(**loaded_json["response"]["players"][0])
        # API returns a list with 1 element which we have to specify [0] in order to map to the data class

    def get_players(self, game_id: int) -> Players:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid={game_id}")
        x = loaded_json["response"]
        return Players(**x)

    def get_game_details(self, game_id: int) -> GameDetails:
        loaded_json = self.__request(f"https://steamspy.com/api.php?request=appdetails&appid={game_id}")
        return GameDetails(**loaded_json)


    def get_game_url(self, game_id: int) -> str:
        game_url = f"https://store.steampowered.com/app/{game_id}"
        return game_url

    def get_user_url(self, user: str) -> str:
        user_url = f"https://steamcommunity.com/id/{user}"
        return user_url

    def get_achievement_url(self, user: str, game_id: int) -> str:
        achievements_url = f"https://steamcommunity.com/id/{user}/stats/{game_id}/achievements/"
        return achievements_url
