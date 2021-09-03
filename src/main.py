from src import steam_api
from steam.steamid import SteamID


def print_game_id():
    game = input('What game would you like to look up? ')
    game_id = steam_api.get_game_id(game)
    if game_id is None:
        print("Game not found")
    else:
        print(game_id)
    main()


def main():
    request = input('What Steam request would you like to make? Options :\n '
                    'Get Game ID'
                    '\n ')
    if request == "Get Game ID":
        print_game_id()
    else:
        print('That is not a valid request')
        main()


main()
