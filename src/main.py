import steam
import discord
from discord.ext import commands
import os
from src.exceptions import GameIsNoneError, UserIsNoneError
from typing import Union
from src import steam_api
from src.utils import formatter
from steam.steamid import SteamID

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    raise Exception('No DISCORD_BOT_TOKEN provided')

bot = commands.Bot(command_prefix = '$')
bot.remove_command('help') #Removes discord's build in help command so we can create a custom one


def return_game_id(game: str) -> int:
    game_id = steam_api.get_game_id(game)
    if game_id is None:
        raise GameIsNoneError("Game not found or was spelt incorrectly.")
    else:
        return game_id

def return_user_id(user: str) -> str:
    user_id = steam_api.get_steam_id(user)
    if user_id is None:
        raise UserIsNoneError("User not found or has a private profile.")
    else:
        return user_id


def return_rarest_achievement(game:str) -> str:
    game_id = return_game_id(game)
    achievement = steam_api.get_rarest_achievement(game_id) #This is a dict
    achievement_name = formatter.format_achievement_name(achievement['name'])
    achievement_percent = formatter.format_achievement_percent(achievement['percent'])
    return f"The rarest achievement is {achievement_name} which {achievement_percent}% of players unlocked"


def return_users_game_playtime(user: str, game: str) -> str:
    user_id = return_user_id(user)
    game_id = return_game_id(game)
    if steam_api.get_users_game_playtime(user_id, game_id) is None:
        total_hours = 0
    else:
        total_hours = formatter.format_users_game_playtime(steam_api.get_users_game_playtime(user_id, game_id))
    return f"{user} has a total of {total_hours} hours played on {game}!"


def return_users_total_platime(user) -> str:
    user_id = return_user_id(user)
    if steam_api.get_users_total_playtime(user_id) is None:
        total_playtime = 0
    else:
        total_playtime = formatter.format_users_total_playtime(steam_api.get_users_total_playtime(user_id))
    return f"{user} has a grand total of {total_playtime} hours played on Steam!"


def return_game_player_count(game: str) -> str:
    game_id = return_game_id(game)
    player_count = formatter.format_numbers_with_comma(steam_api.get_game_player_count(game_id))
    return f"{game} has a current player count of {player_count}"


def main():
    @bot.command()
    async def help(ctx):
        embed = discord.Embed(title="Steamy Commands",
                              url="https://github.com/JDGiardino/Steamy/blob/main/README.md",
                              description="Below are the exact Steamy commands you can use in-channel :",
                              color = discord.Colour.blue())
        embed.set_thumbnail(url="https://imgur.com/KtPxVZS.jpeg")
        embed.add_field(name='$rarest_achievement "GAME NAME"', value='Prints the least unlocked achievement for a given game', inline=False)
        embed.add_field(name='$users_game_playtime "USER NAME" "GAME NAME"', value='Prints a given user\'s played hours on a given game', inline=False)
        embed.add_field(name='$users_total_playtime "USER NAME"', value='Prints a given user\'s total played hours on Steam', inline=False)
        embed.add_field(name='$game_player_count "GAME NAME"', value='Prints the current player count for a given game', inline=False)
        await ctx.message.author.send(embed=embed)
        await ctx.send('A guide on commands for Steamy has been sent to you in a private message.')

    @bot.command(
        name = "game_id", description = "Prints the ID for a given game"
    )
    async def game_id(ctx, arg: str):
        try:
            await ctx.send(return_game_id(arg))
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name = "user_id", description = "Prints the ID for a given user"
    )
    async def user_id(ctx, arg: str):
        try:
            await ctx.send(return_user_id(arg))
        except UserIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name = "rarest_achievement", description = "Prints the least unlocked achievement for a given game"
    )
    async def rarest_achievement(ctx, arg: str):
        try:
            await ctx.send(return_rarest_achievement(arg))
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name = "users_game_playtime", description = "Prints a given user's played hours on a given game"
    )
    async def users_game_playtime(ctx, arg1: str, arg2: str):
        try:
            await ctx.send(return_users_game_playtime(arg1, arg2))
        except (GameIsNoneError, UserIsNoneError) as exc:
            await ctx.send(exc)

    @bot.command(
        name = "users_total_playtime", description = "Prints a given user's total played hours on Steam"
    )
    async def users_total_playtime(ctx, arg: str):
        try:
            await ctx.send(return_users_total_platime(arg))
        except (GameIsNoneError, UserIsNoneError) as exc:
            await ctx.send(exc)

    @bot.command(
        name = "game_player_count", description = "Prints the current player count for a given game"
    )
    async def game_player_count(ctx, arg: str):
        try:
            await ctx.send(return_game_player_count(arg))
        except (GameIsNoneError) as exc:
            await ctx.send(exc)

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Opps! You didn't include an argument with the command")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("This command was not found.  Please make sure your command is valid")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the appropriate permissions to run this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have sufficient permissions!")
        else:
            await ctx.send(f"Ran into an error \"{error}\"  This is unexpected, please report this to the bot creator")

    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
      main()
