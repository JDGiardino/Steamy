import steam
from src import steam_api
from steam.client import SteamClient


def return_game_id():
    game = input('What game would you like to look up? ')
    game_id = steam_api.get_game_id(game)
    if game_id is None:
        print("Game not found")
    else:
        return game_id


def main():
    request = input('What Steam request would you like to make? Options :\n '
                    'Get game ID\n '
                    'Get rarest achivement in a game\n ')
    if request == "Get Game ID":
        print(return_game_id())
        main()
    elif request == "Get rarest achivement in a game":
        print(steam_api.get_rarest_achivement(return_game_id()))
        main()
    else:
        print('That is not a valid request')
        main()


if __name__ == "__main__":
      main()
