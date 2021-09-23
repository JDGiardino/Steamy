import re
import string

def format_achievement_name(achievement_name: str) -> str:
    numbers = r'[0-9]'
    achievement_name = re.sub(numbers, '', achievement_name) #Uses Regex to replace numbers with empty string
    achievement_name = achievement_name.replace("_", " ")
    achievement_name = string.capwords(achievement_name)
    return achievement_name


def format_achievement_percent(achievement_percent: int) -> int:
    achievement_percent = round(achievement_percent, 2)
    return achievement_percent


def format_users_playtime(game_playtime: dict) -> int:
    if game_playtime is None:
        return 0
    else:
        total_hours = game_playtime["playtime_forever"] / 60
        return round(total_hours, 2)
