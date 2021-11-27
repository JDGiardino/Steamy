from src.exceptions import GameIsNoneError, UserIsNoneError
from src import steam_api
from src.utils import formatter
from src.models.RarestAchievement import RarestAchievement
from src.models.Playtime import Playtime


def get_game_id(game_name: str) -> int:
    game = steam_api.get_game(game_name)
    if game is None:
        raise GameIsNoneError("Game not found or was spelled incorrectly.")
    else:
        return game.appid


def get_user_id(user: str) -> int:
    user_id = steam_api.get_steam_id(user)
    if user_id is None:
        raise UserIsNoneError("User not found or has a private profile.")
    else:
        return user_id


def rarest_achievement_desc(game_name: str) -> RarestAchievement:
    game_id = get_game_id(game_name)
    achievement_percent = steam_api.get_achievement_percent(game_id)
    achievement_details = steam_api.get_achievement_details(achievement_percent.name, game_id)
    name = achievement_details.displayName
    achievement_description = achievement_details.description
    percent = formatter.format_achievement_percent(achievement_percent.percent)
    icon = achievement_details.icon
    achievement = f"The rarest achievement in {game_name} is {name} which {percent}% of players unlocked "
    description = f"The achievement description is \"{achievement_description}\""
    return RarestAchievement(name=name, achievement=achievement, description=description, icon=icon)


def users_game_playtime_desc(user: str, game_name: str) -> Playtime:
    user_id = get_user_id(user)
    game_id = get_game_id(game_name)
    if steam_api.get_game_playtimes(user_id, game_id) is None:
        total_hours = 0
    else:
        playtime = steam_api.get_game_playtimes(user_id, game_id)
        total_hours = formatter.format_users_game_playtime(playtime.playtime_forever)
    icon = steam_api.get_game_icon(game_id)
    game_url = f"https://store.steampowered.com/app/{game_id}"
    user_url = f"https://steamcommunity.com/id/{user}"
    description = f"[{user}]({user_url}) has a total of {total_hours} hours played on [{game_name}]({game_url})!"
    # This uses special Discord syntax to make user and game_name into a clickable URL.  [notation_here](link_here)
    return Playtime(name=game_name, description=description, icon=icon)


def users_total_playtime_desc(user) -> str:
    user_id = get_user_id(user)
    if steam_api.get_users_total_playtime(user_id) is None:
        total_playtime = 0
    else:
        total_playtime = formatter.format_users_total_playtime(steam_api.get_users_total_playtime(user_id))
    return f"{user} has a grand total of {total_playtime} hours played on Steam!"


def game_player_count_desc(game_name: str) -> str:
    game_id = get_game_id(game_name)
    players = steam_api.get_players(game_id)
    player_count = formatter.format_numbers_with_comma(players.player_count)
    return f"{game_name} has a current player count of {player_count}"
