from src.models.Game import Game
from src.steam_api import SteamApi
import unittest.mock
# Tests are ran with poetry run pytest -vvvv or poetry run pytest -k test_function_name


def test_get_game_icon():
    game_id = 5
    expected_game_icon_url = "https://steamcdn-a.akamaihd.net/steam/apps/5/header.jpg"

    steam_api = SteamApi()
    actual_game_icon_url = steam_api.get_game_icon(game_id)

    assert expected_game_icon_url == actual_game_icon_url

# pytest syntax for buckets.  First test in bucket one , second another, etc.
def test_get_game():
    mock_response = unittest.mock.Mock()
    mock_response.text = '{"applist":{"apps":[{"appid":1,"name":"joes_game"},{"appid":2,"name":"nicholas_game"}]}}'
    # This part needs to come first because we know the data we want to mock for the response
    mock_request_client = unittest.mock.Mock()
    mock_request_client.request.return_value = mock_response
    # This part needs to come second because we need to define our response before we call it
    # When you call request on mock request client, the return value is that mock_response instance

    steam_api = SteamApi(mock_request_client)
    # print(mock_response) = <Mock name='mock.request()' id='4490353344'>
    # print(mock_response.text) = {"applist":{"apps":[{"appid":1,"name":"joes_game"},{"appid":2,"name":"nicholas_game"}]}}
    # print(mock_request_client) = <Mock id='4490353776'>
    # print(mock_request_client.request()) = <Mock name='mock.request()' id='4490353344'>
    # response = mock_request_client.request()
    # print(response.text) = {"applist":{"apps":[{"appid":1,"name":"joes_game"},{"appid":2,"name":"nicholas_game"}]}}
    # This needs to mimic the request for the data
    actual_get_game = steam_api.get_game("joes_game")
    expected_get_game = Game(name="joes_game", appid=1)

    assert actual_get_game == expected_get_game



