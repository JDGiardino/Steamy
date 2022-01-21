import pytest
from unittest.mock import patch
import bot_helper
from src.exceptions import GameIsNoneError
from src.exceptions import UserIsNoneError
from src.models.Game import Game


class TestGetGameID:
    @staticmethod
    #order of decorators
    @patch("bot_helper.steam_api")
    # Patch is the first function that's called, look for this module given, and pass it instead the mock data
    def test_when_game_does_not_exist(mock_steam_api):
        # patch is giving us an instance of a mock that it created from the given module
        mock_steam_api.get_game.return_value = None
        # we are now defining our fake data for the mock.  When you call get game on this mock, this is the return data
        with pytest.raises(GameIsNoneError):
            # with (context manager) we're using special pytest function.  We expect a GameIsNoneError exception to be raised when given the above
            bot_helper.get_game_id('a_game_that_doesnt_exist')
            # this actually doesn't matter

    @staticmethod
    @patch("bot_helper.steam_api")
    def test_when_game_does_exist(mock_steam_api):
        mock_steam_api.get_game.return_value = Game(name='Apex Legends', appid=1172470)

        actual_game_id = bot_helper.get_game_id('Apex Legends')
        expected_game_id = 1172470

        assert actual_game_id == expected_game_id


class TestGetUserID:
    @staticmethod
    @patch("bot_helper.steam_api")
    def test_when_user_does_not_exist(mock_steam_api):
        mock_steam_api.get_steam_id.return_value = None
        with pytest.raises(UserIsNoneError):
            bot_helper.get_user_id('a_user_that_doesnt_exist')

    @staticmethod
    @patch("bot_helper.steam_api")
    def test_when_user_does_exist(mock_steam_api):
        mock_steam_api.get_steam_id.return_value = 76561198094936897

        actual_user_id = bot_helper.get_user_id('xAmpharosx')
        expected_user_id = 76561198094936897

        assert actual_user_id == expected_user_id
