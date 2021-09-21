import steam
import re
import string
from src import steam_api
from steam.client import SteamClient


def return_game_id() -> int:
    game = input('What game would you like to look up? ')
    game_id = steam_api.get_game_id(game)
    if game_id is None:
        print("Game not found")
    else:
        return game_id


def return_rarest_achievement() -> str:
    rarest_achievement = steam_api.get_rarest_achievement(return_game_id()) #This is a dict

    numbers = r'[0-9]'
    rarest_achievement_name = re.sub(numbers, '', rarest_achievement['name'])
    rarest_achievement_name = rarest_achievement_name.replace("_"," ")
    rarest_achievement_name = string.capwords(rarest_achievement_name)

    rarest_achievement_percent = round(rarest_achievement['percent'], 2)

    return f"The rarest achievement is {rarest_achievement_name} which {rarest_achievement_percent}% of players unlocked"


def main():
    request = input('What Steam request would you like to make? Options :\n '
                    'Get game ID\n '
                    'Get rarest achievement in a game\n ')
    if request == "Get game ID":
        print(return_game_id())
        main()
    elif request == "Get rarest achievement in a game":
        print(return_rarest_achievement())
        main()
    else:
        print('That is not a valid request')
        main()


if __name__ == "__main__":
      main()
