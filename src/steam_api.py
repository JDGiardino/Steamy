import steam
import json
import os

from cachetools import cached, TTLCache
from typing import Union, Optional
from src.models.AchievementPercent import AchievementPercent
from src.models.AchievementDetails import AchievementDetails
from src.models.PlayerAchievements import PlayerAchievements
from src.models.TwoWeekStats import TwoWeekStats
from src.models.PlayerSummary import PlayerSummary
from src.models.Game import Game
from src.models.Players import Players
from src.models.Playtime import Playtime
from src.models.GameDetails import GameDetails
from src.utils.requests_retry_client import RequestsRetryClient
from steam.steamid import SteamID


class SteamApi(object):

    def __init__(self, request_client=None):
        self.STEAM_API_KEY = os.environ.get('STEAM_API_KEY')
        # Obtain a Steam Web API Key from https://steamcommunity.com/dev/apikey
        if not self.STEAM_API_KEY:
            raise Exception('No STEAM_API_KEY provided')
        if request_client is None:
            self.request_client = RequestsRetryClient()
        else:
            self.request_client = request_client

    def __request(self, url: str) -> dict:
        response = self.request_client.request(method='GET', url=url)
        return json.loads(response.text)

    @staticmethod
    def get_steam_id(community_name: str) -> int:
        return steam.steamid.from_url(f'https://steamcommunity.com/id/{community_name}')
        # This takes a Steam community URL for a profile and converts it to a SteamID

    def get_game(self, game_name: str) -> Optional[Game]:
        json_app_list = self.__request("https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
        for x in json_app_list["applist"]["apps"]:
            if game_name == x['name']:
                return Game(**x)
        return None

    def get_achievement_percent(self, game_id: int) -> Union[None, AchievementPercent]:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={game_id}")
        if loaded_json == {}:
            return None
        # API returns empty json for a game_id passed with no achievements.  Above 2 lines catches this case.
        else:
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
            return None

    @staticmethod
    def get_game_icon(game_id: int) -> str:
        return f"https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/header.jpg"

    @staticmethod
    def get_steam_icon() -> str:
        return "https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/steam-icon.png"

    def get_player_achievements(self, user_id: int, game_id: int) -> Union[str, PlayerAchievements]:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={self.STEAM_API_KEY}&appid={game_id}&steamid={user_id}")
        if "error" in loaded_json["playerstats"] and loaded_json["playerstats"]["error"] == "Requested app has no stats":
            return 'No_Game'
        # This catches when API returns differently for a game_id passed a the user_id has never played.
        elif "error" in loaded_json["playerstats"] and loaded_json["playerstats"]["error"] == "Profile is not public":
            return 'Private_Profile'
        # This catches when API returns differently for a user_id that has achievements not public on their profile.
        elif loaded_json["playerstats"]["success"] and not "achievements" in loaded_json["playerstats"]:
            return 'No_Achievements'
        else:
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

    def get_users_two_week_stats(self, user_id: int) -> Union[None, TwoWeekStats]: # add tests
        loaded_json = self.__request(
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.STEAM_API_KEY}&steamid={user_id}&format=json")
        playtime = loaded_json["response"].get("games")
        if playtime is None:
            return None  # This catches if the json object does not have the assumed nested items
        two_week_playtime = 0
        two_week_games = []
        for x in playtime:
            if "playtime_2weeks" in x:
                two_week_playtime += x["playtime_2weeks"]
                two_week_games.append(x["appid"])
        return TwoWeekStats(two_week_playtime=two_week_playtime, two_week_games=two_week_games)

    def get_player_summaries(self, user_id: int) -> PlayerSummary:
        loaded_json = self.__request(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.STEAM_API_KEY}&steamids={user_id}")
        return PlayerSummary(**loaded_json["response"]["players"][0])
        # API returns a list with 1 element which we have to specify [0] in order to map to the data class

    def get_players(self, game_id: int) -> Players:
        loaded_json = self.__request(f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?format=json&appid={game_id}")
        x = loaded_json["response"]
        return Players(**x)

    @cached(cache=TTLCache(maxsize=33, ttl=100))
    def get_top_100_games(self) -> list[dict[str: str]]:
        top_100_in_2_weeks = self.__request(f"https://steamspy.com/api.php?request=top100in2weeks").values()
        # .values() turns the returned dict into a list
        top_100 = []
        for x in top_100_in_2_weeks:
            players = self.get_players(x["appid"])
            top_100.append({"appid": x["appid"], "name": x["name"], "player_count": players.player_count})
        sorted_top_100 = sorted(top_100, key=lambda i: i["player_count"], reverse=True)
        return sorted_top_100

    def get_game_details(self, game_id: int) -> GameDetails:
        loaded_json = self.__request(f"https://steamspy.com/api.php?request=appdetails&appid={game_id}")
        return GameDetails(**loaded_json)

    @staticmethod
    def get_game_url(game_id: int) -> str:
        game_url = f"https://store.steampowered.com/app/{game_id}"
        return game_url

    @staticmethod
    def get_user_url(user: str) -> str:
        user_url = f"https://steamcommunity.com/id/{user}"
        return user_url

    @staticmethod
    def get_achievement_url(user: str, game_id: int) -> str:
        achievements_url = f"https://steamcommunity.com/id/{user}/stats/{game_id}/achievements/"
        return achievements_url
