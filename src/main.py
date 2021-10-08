import steam
import discord
from discord.ext import commands
import os
from typing import Union
from src import steam_api
from src.utils import formatter
from steam.steamid import SteamID

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    raise Exception('No DISCORD_BOT_TOKEN provided')

bot = commands.Bot(command_prefix = '$')


def return_game_id(game: str) -> Union [int,None]:
    game_id = steam_api.get_game_id(game)
    if game_id is None:
        return "Game not found"
    else:
        return game_id


def return_rarest_achievement(game:str) -> str:
    achievement = steam_api.get_rarest_achievement(return_game_id(game)) #This is a dict
    achievement_name = formatter.format_achievement_name(achievement['name'])
    achievement_percent = formatter.format_achievement_percent(achievement['percent'])
    return f"The rarest achievement is {achievement_name} which {achievement_percent}% of players unlocked"


def return_users_game_playtime(user: str, game: str) -> str:
    user_id = steam_api.get_steam_id(user)
    if user_id is None:
        return "User not found or has a private profile"
    else:
        game_id = return_game_id(game)
        if steam_api.get_users_game_playtime(user_id, game_id) is None:
            total_hours = 0
        else:
            total_hours = formatter.format_users_game_playtime(steam_api.get_users_game_playtime(user_id, game_id))
        return f"{user} has a total of {total_hours} hours played on {game}!"


def return_users_total_platime(user) -> str:
    user_id = steam_api.get_steam_id(user)
    if user_id is None:
        return "User not found or has a private profile"
    else:
        total_playtime = formatter.format_users_total_playtime(steam_api.get_users_total_playtime(user_id))
        return f"{user} has a grand total of {total_playtime} hours played on Steam!"


def main():
    @bot.command()
    async def game_id(ctx, arg: str):
        await ctx.send(return_game_id(arg))

    @game_id.error
    async def game_id(ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send("You haven't provided a game.  Please enter a game after '$game_id'")

    @bot.command()
    async def rarest_achievement(ctx, arg: str):
        await ctx.send(return_rarest_achievement(arg))

    @bot.command()
    async def users_game_playtime(ctx, arg1: str, arg2: str):
        await ctx.send(return_users_game_playtime(arg1, arg2))

    @bot.command()
    async def users_total_playtime(ctx, arg:str):
        await ctx.send(return_users_total_platime(arg))

    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
      main()
