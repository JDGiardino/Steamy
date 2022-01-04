# Steamy

This code powers a Discord bot that uses the Steam API to make requests for various game statistics and user data.

## Bot Setup 
[IN PROGRESS] Add walkthrough for setup



## Bot Commands
The following lists all the commands Steamy bot can preform and examples of their output:
- `$achievement GAME_NAME` - This command posts to the server the rarest achievement for the given game name.
- `$game GAME_NAME` - This command posts to the server the player count and rank in top played games for the given game name.
- `$help` - This command sends a direct message to user who called it, with a list of all commands Steamy can preform. 
- `$top NUMBER` - This command posts to the server the top played games by player count up to the given number(No higher than 100).
- `$user USER_NAME` - This command posts to the server the total played hours on Steam for the given Steam user name.
- `$users_game "USERS_NAME" "GAME_NAME"` - This command posts to the server a given user's played hours and unlocked achievements for a given game.
- `$user_id` USER_NAME - This command posts to the server the ID for a given Steam user name.