import steam
from src import steam_api
from src.utils import formatter
from steam.steamid import SteamID


def return_game_id() -> int:
    game = input('What game would you like to look up? ')
    game_id = steam_api.get_game_id(game)
    if game_id is None:
        return "Game not found"
    else:
        return game_id

def return_users_playtime() -> str:
    user = input('What user would you like to look up? ')
    user_id = steam_api.get_steam_id(user)
    if user_id is None:
        return "User not found or has a private profile"
    else:
        game = return_game_id()
        total_hours = formatter.format_users_playtime(steam_api.get_users_playtime(user_id, game))
        return f"{user} has a total of {total_hours} hours played!"


def return_rarest_achievement() -> str:
    achievement = steam_api.get_rarest_achievement(return_game_id()) #This is a dict
    achievement_name = formatter.format_achievement_name(achievement['name'])
    achievement_percent = formatter.format_achievement_percent(achievement['percent'])
    return f"The rarest achievement is {achievement_name} which {achievement_percent}% of players unlocked"


def main():
    request = input('What Steam request would you like to make? Options :\n '
                    'Get game ID\n '
                    'Get a user\'s playtime hours on a game\n '
                    'Get rarest achievement in a game\n ')
    if request == "Get game ID":
        print(return_game_id())
        main()
    elif request == "Get a user\'s playtime hours on a game":
        print(return_users_playtime())
        main()
    elif request == "Get rarest achievement in a game":
        print(return_rarest_achievement())
    else:
        print('That is not a valid request')
        main()


if __name__ == "__main__":
      main()
