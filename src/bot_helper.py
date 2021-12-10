import datetime

from src.exceptions import GameIsNoneError, UserIsNoneError
from src.steam_api import SteamApi
from src.utils import formatter
from src.models.RarestAchievement import RarestAchievement
from src.models.Stats import Stats

steam_api = SteamApi()  # Global variable to this module that is instaniating a SteamApi class.


def get_game_id(game_name: str) -> int:
    game = steam_api.get_game(game_name)
    if game is None:
        raise GameIsNoneError(f"{game_name} not found or was spelled incorrectly.")
    else:
        return game.appid


def get_user_id(user: str) -> int:
    user_id = steam_api.get_steam_id(user)
    if user_id is None:
        raise UserIsNoneError(f"{user} not found or has a private profile.")
    else:
        return user_id


def rarest_achievement_desc(game_name: str) -> RarestAchievement:
    game_id = get_game_id(game_name)
    achievement_percent = steam_api.get_achievement_percent(game_id)
    achievement_details = steam_api.get_achievement_details(achievement_percent.name, game_id)
    name = achievement_details.displayName
    achievement_description = achievement_details.description
    percent = formatter.format_achievement_percent(achievement_percent.percent)
    achievement = f"The rarest achievement in [{game_name}]({steam_api.get_game_url(game_id)}) is {name} which {percent}% of players unlocked "
    description = f"The achievement description is \"{achievement_description}\""
    return RarestAchievement(name=name, achievement=achievement, description=description, icon=achievement_details.icon)


def users_game_stats(user: str, game_name: str) -> Stats:
    user_id = get_user_id(user)
    game_id = get_game_id(game_name)
    if steam_api.get_game_playtimes(user_id, game_id) is None:
        total_hours = 0
    else:
        playtime = steam_api.get_game_playtimes(user_id, game_id)
        total_hours = formatter.format_users_game_playtime(playtime.playtime_forever)
    description1 = f"[{user}]({steam_api.get_user_url(user)}) has a total of {total_hours} hours played on [{game_name}]({steam_api.get_game_url(game_id)})! "
    # This uses special Discord syntax to make user and game_name into a clickable URL.  [notation_here](link_here)
    player_achievements = steam_api.get_player_achievements(user_id, game_id)
    description2 = f"{user}({steam_api.get_user_url(user)}) has unlocked [{player_achievements.unlocked}/{player_achievements.total} achievements]({steam_api.get_achievement_url})!"
    return Stats(name=game_name, description1=description1, description2=description2, icon=steam_api.get_game_icon(game_id))


def users_stats(user) -> Stats:
    user_id = get_user_id(user)
    if steam_api.get_users_total_playtime(user_id) is None:
        total_playtime = 0
    else:
        total_playtime = formatter.format_users_total_playtime(steam_api.get_users_total_playtime(user_id))
    player_summary = steam_api.get_player_summaries(user_id)
    description1 = f"[{user}]({player_summary.profileurl}) has a grand total of {total_playtime} hours played on Steam!"
    description2 = f"{user}({player_summary.profileurl})'s profile was created on {datetime.datetime.fromtimestamp(player_summary.timecreated)}"
    return Stats(name=user, description1=description1, description2=description2, icon=player_summary.avatarfull)


def game_desc(game_name: str) -> Stats:
    game_id = get_game_id(game_name)
    players = steam_api.get_players(game_id)
    player_count = formatter.format_numbers_with_comma(players.player_count)
    game_details = steam_api.get_game_details(game_id)
    description1 = f"[{game_name}]({steam_api.get_game_url(game_id)}) is developed by {game_details.developer} and published by {game_details.publisher}"
    description2 = f"[{game_name}]({steam_api.get_game_url(game_id)}) has a current player count of {player_count}"
    return Stats(name=game_name, description1=description1, description2=description2, icon=steam_api.get_game_icon(game_id))

