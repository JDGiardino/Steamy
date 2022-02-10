def format_achievement_percent(achievement_percent: float) -> float:
    achievement_percent = round(achievement_percent, 2)
    return achievement_percent


def format_users_game_playtime(game_playtime: int) -> str:
    total_hours: float = game_playtime / 60
    return format_numbers_with_comma(round(total_hours, 2))


def format_users_playtime(total_playtime: float) -> str:
    total_hours = total_playtime / 60
    return format_numbers_with_comma(round(total_hours, 2))


def format_numbers_with_comma(number: int) -> str:
    formatted_number = "{:,}".format(number)
    return formatted_number
