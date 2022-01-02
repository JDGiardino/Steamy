from dataclasses import dataclass
from dataclasses import field
from typing import Optional


@dataclass(frozen=True)
class PlayerSummary:
    steamid: str
    # 64bit SteamID of the user
    personaname: str
    # The player's persona name (display name)
    profileurl: str
    # The full URL of the player's Steam Community profile.
    avatar: str
    # The full URL of the player's 32x32px avatar. If the user hasn't configured an avatar, this will be the default
    # ? avatar.
    avatarmedium: str
    # The full URL of the player's 64x64px avatar. If the user hasn't configured an avatar, this will be the default
    # ? avatar.
    avatarfull: str
    # The full URL of the player's 184x184px avatar. If the user hasn't configured an avatar, this will be the
    # default ? avatar.
    personastate: int
    # The user's current status. 0 - Offline, 1 - Online, 2 - Busy, 3 - Away, 4 - Snooze, 5 - looking to trade,
    # 6 - looking to play. If the player's profile is private, this will always be "0", except if the user has set
    # his status to looking to trade or looking to play, because a bug makes those status appear even if the profile
    # is private.
    communityvisibilitystate: int
    # This represents whether the profile is visible or not, and if it is visible, why you are allowed to see it.
    # Note that because this WebAPI does not use authentication, there are only two possible values returned: 1 - the
    # profile is not visible to you (Private, Friends Only, etc), 3 - the profile is "Public", and the data is
    # visible. Mike Blaszczak's post on Steam forums says, "The community visibility state this API returns is
    # different than the privacy state. It's the effective visibility state from the account making the request to
    # the account being viewed given the requesting account's relationship to the viewed account."
    avatarhash: str
    primaryclanid: str
    # The player's primary group, as configured in their Steam Community profile.
    timecreated: int
    # The time the player's account was created.
    personastateflags: int
    commentpermission: Optional[int] = field(default=None) # Using defaults for optional fields that may not appear in the API call
    # If set, indicates the profile allows public comments.
    lastlogoff: Optional[int] = field(default=None)
    # The last time the user was online, in unix time.
    profilestate: Optional[int] = field(default=None)
    # If set, indicates the user has a community profile configured (will be set to '1')
    realname: Optional[str] = field(default=None)
    # The player's "Real Name", if they have set it
    gameid: Optional[int] = field(default=None)
    # If the user is currently in-game, this value will be returned and set to the gameid of that game.
    gameserverip: Optional[int] = field(default=None)
    # The ip and port of the game server the user is currently playing on, if they are playing on-line in a game
    # using Steam matchmaking. Otherwise will be set to "0.0.0.0:0".
    gameextrainfo: Optional[str] = field(default=None)
    # If the user is currently in-game, this will be the name of the game they are playing. This may be the name of a
    # non-Steam game shortcut.
    loccountrycode: Optional[int] = field(default=None)
    # If set on the user's Steam Community profile, The user's country of residence, 2-character ISO country code
    locstatecode: Optional[int] = field(default=None)
    # If set on the user's Steam Community profile, The user's state of residence
    loccityid: Optional[int] = field(default=None)
    # An internal code indicating the user's city of residence. A future update will provide this data in a more
    # useful way.