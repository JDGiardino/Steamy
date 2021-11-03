class GameIsNoneError(Exception):
    """Raised when a string game is passed that cannot be found by Steam API."""


class UserIsNoneError(Exception):
    """Raised when a string user is passed that cannot be found by Steam API."""
