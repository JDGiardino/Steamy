import requests
import json
import time


def get_request(url: str, parameters=None):
    try:
        response = requests.get(url=url, params=parameters)
    except requests.exceptions.SSLError as error:
        print('SSL Error:', error, 'waiting 10 seconds...')
        time.sleep(10)
        print('Retrying')
        return get_request(url, parameters)
    if response:
        return response
    else:
        print('No response, waiting 10 seconds...')
        time.sleep(10)
        print('Retrying')
        return get_request(url, parameters)


def get_game_id(game: str):
    response = get_request(url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/")
    json_app_list = json.loads(response.text)  # Load the JSON data
    for x in json_app_list["applist"]["apps"]:
        if game == x['name']:
            return x['appid']
