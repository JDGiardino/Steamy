from src import steam_api
from steam.steamid import SteamID


def game_id():
    game = input('What game would you like to look up? ')
    print(steam_api.get_game_id(game))
    main()


def main():
    request = input('What Steam request would you like to make? Options :\n '
          'Get Game ID')
    if request == "Get Game ID":
        game_id()
    else:
        print('That is not a valid request')
        main()


main()
