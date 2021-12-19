import datetime
import itertools

from src.exceptions import GameIsNoneError, UserIsNoneError, ExceedingTopGamesMax, GameHasNoAchievements
from src.steam_api import SteamApi
from src.utils import formatter
from src.models.RarestAchievement import RarestAchievement
from src.models.Stats import Stats

steam_api = SteamApi()  # Global variable to this module that is instantiating a SteamApi class.


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
    if achievement_percent is None:
        raise GameHasNoAchievements(f"{game_name} does not have any achievements to unlock.")
    else:
        achievement_details = steam_api.get_achievement_details(achievement_percent.name, game_id)
        name = achievement_details.displayName
        achievement_description = achievement_details.description
        percent = formatter.format_achievement_percent(achievement_percent.percent)
        achievement = f"The rarest achievement in [{game_name}]({steam_api.get_game_url(game_id)}) is {name} which {percent}% of players unlocked "
        # This uses special Discord syntax to make user and game_name into a clickable URL.  [notation_here](link_here)
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
    description1 = f"[{user}]({steam_api.get_user_url(user)}) has a total of {total_hours} hours " \
                   f"played on [{game_name}]({steam_api.get_game_url(game_id)})! "
    player_achievements = steam_api.get_player_achievements(user_id, game_id)
    if player_achievements == 0:
        description2 = f"[{user}]({steam_api.get_user_url(user)}) has unlocked 0 achievements"
    elif player_achievements == 1:
        description2 = f"[{game_name}]({steam_api.get_game_url(game_id)}) does not have any achievements to unlock."
    else:
        description2 = f"[{user}]({steam_api.get_user_url(user)}) has unlocked " \
                       f"[{player_achievements.unlocked}/{player_achievements.total} achievements]" \
                       f"({steam_api.get_achievement_url(user, game_id)})!"
    return Stats(name=game_name, description1=description1, description2=description2, icon=steam_api.get_game_icon(game_id))


def users_stats(user) -> Stats:
    user_id = get_user_id(user)
    if steam_api.get_users_total_playtime(user_id) is None:
        total_playtime = 0
    else:
        total_playtime = formatter.format_users_total_playtime(steam_api.get_users_total_playtime(user_id))
    player_summary = steam_api.get_player_summaries(user_id)
    description1 = f"[{user}]({player_summary.profileurl}) has a grand total of {total_playtime} hours played on Steam!"
    description2 = f"[{user}]({player_summary.profileurl})'s profile was created on " \
                   f"{datetime.datetime.fromtimestamp(player_summary.timecreated)}"
    return Stats(name=user, description1=description1, description2=description2, icon=player_summary.avatarfull)


def game_desc(game_name: str) -> Stats:
    game_id = get_game_id(game_name)
    game_details = steam_api.get_game_details(game_id)
    players = steam_api.get_players(game_id)
    player_count = formatter.format_numbers_with_comma(players.player_count)
    description1 = f"[{game_name}]({steam_api.get_game_url(game_id)}) is developed by {game_details.developer} " \
                   f"and published by {game_details.publisher}."
    description2 = f"[{game_name}]({steam_api.get_game_url(game_id)}) has a current player count of {player_count}!\n" \
                   f"[{game_name}]({steam_api.get_game_url(game_id)}) is not currently in the top 100 most played games on Steam."
    top100games = steam_api.get_top_100_games()
    for x in top100games:
        if x["name"] == game_name:
            game_rank = top100games.index(x) + 1
            description2 = f"[{game_name}]({steam_api.get_game_url(game_id)}) has a current player count of {player_count}!\n " \
                           f"[{game_name}]({steam_api.get_game_url(game_id)}) is currently the number {game_rank} most played game on Steam!"
    return Stats(name=game_name, description1=description1, description2=description2, icon=steam_api.get_game_icon(game_id))


def get_top_x_games(x: int) -> Stats:
    if x > 100:
        raise ExceedingTopGamesMax("Can only search up to a maximum of the top 100 games.")
    else:
        top100games = steam_api.get_top_100_games()[:x]
        title = f"Top {x} Games by Current Players"
        description1 = f"The following is currently the top {x} played games on Steam!"
        description2 = ""
        for game in top100games:
            description2 += f'#{top100games.index(game) + 1} {game["name"]}'\
                            f' with {formatter.format_numbers_with_comma(game["player_count"])} players\n'
        return Stats(name=title, description1=description1, description2=description2, icon=steam_api.get_steam_icon())


if __name__ == "__main__":
    rarest_achievement_desc("Fallout 4")