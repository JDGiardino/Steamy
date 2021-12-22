class GameIsNoneError(Exception):
    """Raised when a string game is passed that cannot be found by Steam API."""


class UserIsNoneError(Exception):
    """Raised when a string user is passed that cannot be found by Steam API."""


class ExceedingTopGamesMax(Exception):
    """Raises when a number over 100 is passed to the get_top_x_games function.  Discord can only return 4096 characters
    so this exception prevents a user from exceeding that"""


class GameHasNoAchievements(Exception):
    """Raises when a game is searched for that has no achievements."""