import pytest
from unittest.mock import patch
import bot_helper
from src.exceptions import GameIsNoneError
from src.exceptions import UserIsNoneError
from src.models.Game import Game

# Tests are ran with poetry run pytest -vvvv or poetry run pytest -k test_function_name


class TestGetGameID:
    # First 2 functions are using two different methods of Patching
    @staticmethod
    @patch("bot_helper.steam_api")
    def test_when_game_does_not_exist(mock_steam_api):
        mock_steam_api.get_game.return_value = None
        with pytest.raises(GameIsNoneError):
            bot_helper.get_game_id('a_game_that_doesnt_exist')

    @staticmethod
    def test_when_game_does_exist():
        with patch("bot_helper.steam_api", spec=["get_game"]) as mock_steam_api:
            mock_steam_api.get_game.return_value = Game(name='Apex Legends', appid=1172470)
            actual_game_id = bot_helper.get_game_id('Apex Legends')
        expected_game_id = 1172470
        assert actual_game_id == expected_game_id


class TestGetUserID:
    @staticmethod
    def test_when_user_does_not_exist():
        with patch("bot_helper.steam_api", spec=["get_steam_id"]) as mock_steam_api:
            mock_steam_api.get_steam_id.return_value = None
        with pytest.raises(UserIsNoneError):
            bot_helper.get_user_id('a_user_that_doesnt_exist')

    @staticmethod
    def test_when_user_does_exist():
        with patch("bot_helper.steam_api", spec=["get_steam_id"]) as mock_steam_api:
            mock_steam_api.get_steam_id.return_value = 76561198094936897
            actual_user_id = bot_helper.get_user_id('xAmpharosx')
        expected_user_id = 76561198094936897

        assert actual_user_id == expected_user_id
