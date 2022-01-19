from src.models.Playtime import Playtime
from src.models.AchievementDetails import AchievementDetails
from src.models.AchievementPercent import AchievementPercent
from src.models.Players import Players
from src.models.Game import Game
from src.models.AchievementPercent import AchievementPercent
from src.models.AchievementDetails import AchievementDetails
from src.models.Playtime import Playtime
from src.steam_api import SteamApi
import unittest.mock


# Tests are ran with poetry run pytest -vvvv or poetry run pytest -k test_function_name


class TestGetSteamID:
    @staticmethod
    def test_when_a_valid_community_name_is_passed():
        community_name = 'xAmpharosx'
        expected_get_steam_id = 76561198094936897  # IDs for user "xAmpharosx"

        steam_api = SteamApi()
        actual_get_steam_id = steam_api.get_steam_id(community_name)

        assert expected_get_steam_id == actual_get_steam_id


class TestGetGame:
    @staticmethod
    def test_when_a_game_exists():
        """Testing the get_game function for when a game is passed that exists within the response.text"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"applist":{"apps":[{"appid":1,"name":"joes_game"},{"appid":2,"name":"nicholas_game"}]}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_get_game = steam_api.get_game("joes_game")
        expected_get_game = Game(name="joes_game", appid=1)

        assert actual_get_game == expected_get_game

    @staticmethod
    def test_when_a_game_doesnt_exist():
        """Testing the get_game function for when a game is passed that DOES NOT exist within the response.text"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"applist":{"apps":[{"appid":1,"name":"joes_game"},{"appid":2,"name":"nicholas_game"}]}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_get_game = steam_api.get_game("sarahs_game")
        expected_get_game = None

        assert actual_get_game == expected_get_game


class TestGetAchievementPercent:
    @staticmethod
    def test_when_a_game_doesnt_have_achievements():
        """Testing the get_achievement_percent function for when a game is passed that DOES NOT have any achievements"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_achievement_percent = steam_api.get_achievement_percent(892970)  # ID for game "Valheim"
        # The passed game id above actually doesn't matter here since tests uses a mock response.  Same for many tests below
        expected_achievement_percent = None

        assert actual_achievement_percent == expected_achievement_percent

    @staticmethod
    def test_when_a_game_has_achievements():
        """Testing the get_achievement_percent function for when a game is passed that has achievements"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"achievementpercentages":{"achievements":[{"name":"NEW_ACHIEVEMENT_3_22",' \
                             '"percent":74.69},{"name":"NEW_ACHIEVEMENT_4_29","percent":0}]}} '
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_achievement_percent = steam_api.get_achievement_percent(1240440)  # ID for game "Halo Infinite"
        expected_achievement_percent = AchievementPercent(name="NEW_ACHIEVEMENT_4_29", percent=0)

        assert actual_achievement_percent == expected_achievement_percent


class TestGetAchievementDetails:
    @staticmethod
    def test_returning_achievement_details():
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"game":{"gameName":"Halo Infinite","gameVersion":"11","availableGameStats":{' \
                             '"achievements":[{"name":"NEW_ACHIEVEMENT_3_22","defaultvalue":0,"displayName":"Clocking ' \
                             'In","hidden":0,"description":"Complete a Daily Challenge.","icon":"fake_url",' \
                             '"icongray":"fake_url"},{"name":"NEW_ACHIEVEMENT_4_29","defaultvalue":0,' \
                             '"displayName":"MEDIC!","hidden":0,"description":"Revive 3 allies in a matchmade ' \
                             'Elimination round.","icon":"fake_url","icongray":"fake_url"}]}}} '
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_achievement_percent = steam_api.get_achievement_details('NEW_ACHIEVEMENT_4_29',
                                                                       1240440)  # Achivement name from and ID for game "Halo Infinite"
        expected_achievement_percent = AchievementDetails(name='NEW_ACHIEVEMENT_4_29', defaultvalue=0,
                                                          displayName='MEDIC!',
                                                          hidden=0,
                                                          description='Revive 3 allies in a matchmade Elimination round.',
                                                          icon='fake_url', icongray='fake_url')

        assert actual_achievement_percent == expected_achievement_percent


class TestGetGamePlaytimes:
    @staticmethod
    def test_when_user_has_no_played_games():
        """Testing when get_game_playtimes function has a user passed that's never played a game on Steam"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"response":{}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_game_playtimes = steam_api.get_game_playtimes(76561197963831971,
                                                             1240440)  # IDs for user "lol" and game "Halo Infinite"
        expected_game_playtimes = None

        assert actual_game_playtimes == expected_game_playtimes

    @staticmethod
    def test_when_user_has_played_a_game():
        """Testing when get_game_playtimes function has a game passed that the given user has played"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"response":{"game_count":256,"games":[{"appid":35700,"playtime_forever":271,' \
                             '"playtime_windows_forever":0,"playtime_mac_forever":0,"playtime_linux_forever":0}, ' \
                             '{"appid":1240440,"playtime_2weeks":735,"playtime_forever":4496,' \
                             '"playtime_windows_forever":4496,"playtime_mac_forever":0,"playtime_linux_forever":0}]}} '
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_game_playtimes = steam_api.get_game_playtimes(76561198094936897,
                                                             1240440)  # IDs for user "xAmpharosx" and game "Halo Infinite"
        expected_game_playtimes = Playtime(appid=1240440, playtime_2weeks=735, playtime_forever=4496,
                                           playtime_windows_forever=4496,
                                           playtime_mac_forever=0, playtime_linux_forever=0)

        assert actual_game_playtimes == expected_game_playtimes

    @staticmethod
    def test_when_user_has_not_played_a_game():
        """Testing when get_game_playtimes function has a game passed that the given user has not played"""

    mock_response = unittest.mock.Mock()
    mock_response.text = '{"response":{"game_count":256,"games":[{"appid":35700,"playtime_forever":271,' \
                         '"playtime_windows_forever":0,"playtime_mac_forever":0,"playtime_linux_forever":0}, ' \
                         '{"appid":1240440,"playtime_2weeks":735,"playtime_forever":4496,' \
                         '"playtime_windows_forever":4496,"playtime_mac_forever":0,"playtime_linux_forever":0}]}} '
    mock_request_client = unittest.mock.Mock()
    mock_request_client.request.return_value = mock_response

    steam_api = SteamApi(mock_request_client)
    actual_game_playtimes = steam_api.get_game_playtimes(76561198094936897,
                                                         1172620)  # IDs for user "xAmpharosx" and game "Sea of Thieves"
    expected_game_playtimes = None

    assert actual_game_playtimes == expected_game_playtimes


class TestGetGameIcon:
    @staticmethod
    def test_url_returns_with_given_game_id():
        game_id = 5
        expected_game_icon_url = "https://steamcdn-a.akamaihd.net/steam/apps/5/header.jpg"

        steam_api = SteamApi()
        actual_game_icon_url = steam_api.get_game_icon(game_id)

        assert expected_game_icon_url == actual_game_icon_url


class TestGetSteamIcon:
    @staticmethod
    def test_get_steam_icon():
        expected_steam_icon = "https://icons.iconarchive.com/icons/papirus-team/papirus-apps/512/steam-icon.png"

        steam_api = SteamApi()
        actual_steam_icon = steam_api.get_steam_icon()

        assert expected_steam_icon == actual_steam_icon


class TestGetPlayerAchievements:
    @staticmethod
    def test_when_requested_app_has_no_stats():
        """Testing when get_player_achievements function has a game passed for a user that the user has not played"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"playerstats":{"error":"Requested app has no stats","success":false}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_player_achievements = steam_api.get_player_achievements(76561198094936897,
                                                                       1172620)  # IDs for user "xAmpharosx" and game "Sea of Thieves"
        expected_player_achievements = 'No_Game'

        assert actual_player_achievements == expected_player_achievements

    @staticmethod
    def test_when_profile_is_not_public():
        """Testing when get_player_achievements function has a user passed with a public profile set"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"playerstats":{"error":"Profile is not public","success":false}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_player_achievements = steam_api.get_player_achievements(76561198004892682,
                                                                       1172620)  # IDs for user "DGamesta" and game "Sea of Thieves"
        expected_player_achievements = 'Private_Profile'

        assert actual_player_achievements == expected_player_achievements

    @staticmethod
    def test_when_user_has_no_achievements():
        """Testing when get_player_achievements function has a game passed that has no unlockable achievements"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"playerstats":{"steamID":"76561198094936897","gameName":"Valheim","success":true}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_player_achievements = steam_api.get_player_achievements(76561198094936897,
                                                                       892970)  # IDs for user "xAmpharosx" and game "Valheim"
        expected_player_achievements = 'No_Achievements'

        assert actual_player_achievements == expected_player_achievements


class TestGetUsersTotalPlaytime:
    @staticmethod
    def test_when_user_has_no_played_games():
        """Testing when get_users_total_playtime function has a user passed that's never played a game on Steam"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"response":{}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_users_total_playtime = steam_api.get_users_total_playtime(76561197963831971)  # ID for user "lol"
        expected_users_total_playtime = None

        assert actual_users_total_playtime == expected_users_total_playtime

    @staticmethod
    def test_when_user_has_played_games():
        """Testing when get_users_total_playtime function has a user passed that has played a game(s) on Steam"""
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"response":{"game_count":2,"games":[{"appid":1593500,"playtime_2weeks":3,' \
                             '"playtime_forever":3,"playtime_windows_forever":3,"playtime_mac_forever":0,' \
                             '"playtime_linux_forever":0},{"appid":1240440,"playtime_forever":358,' \
                             '"playtime_windows_forever":358,"playtime_mac_forever":0,"playtime_linux_forever":0}]}} '
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_users_total_playtime = steam_api.get_users_total_playtime(76561198094936897)  # ID for user "xAmpharosx"
        expected_users_total_playtime = 361

        assert actual_users_total_playtime == expected_users_total_playtime


class TestGetPlayers:
    @staticmethod
    def test_when_valid_game_passed():
        mock_response = unittest.mock.Mock()
        mock_response.text = '{"response":{"player_count":119140,"result":1}}'
        mock_request_client = unittest.mock.Mock()
        mock_request_client.request.return_value = mock_response

        steam_api = SteamApi(mock_request_client)
        actual_players = steam_api.get_players(1172470)  # ID for game "Apex Legends"
        expected_players = Players(player_count=119140, result=1)

        assert actual_players == expected_players
