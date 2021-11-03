import re
import string


def format_achievement_name(achievement_name: str) -> str:
    numbers = r'[0-9]'
    achievement_name = re.sub(numbers, '', achievement_name)  # Uses Regex to replace numbers with empty string
    achievement_name = achievement_name.replace("_", " ")
    achievement_name = string.capwords(achievement_name)
    return achievement_name


def format_achievement_percent(achievement_percent: float) -> float:
    achievement_percent = round(achievement_percent, 2)
    return achievement_percent


def format_users_game_playtime(game_playtime: int) -> str:
    total_hours: float = game_playtime / 60
    return format_numbers_with_comma(round(total_hours, 2))


def format_users_total_playtime(total_playtime: float) -> str:
    total_hours = total_playtime / 60
    return format_numbers_with_comma(round(total_hours, 2))


def format_numbers_with_comma(number: int) -> str:
    formatted_number = "{:,}".format(number)
    return formatted_number
