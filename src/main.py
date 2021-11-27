import discord
from discord.ext import commands
import os

import bot_helper
from src.exceptions import GameIsNoneError, UserIsNoneError
from src import steam_api

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    raise Exception('No DISCORD_BOT_TOKEN provided')

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')  # Removes discord's build in help command so we can create a custom one


def main():
    @bot.command()
    async def help(ctx):
        embed = discord.Embed(title="Steamy Commands",
                              url="https://github.com/JDGiardino/Steamy/blob/main/README.md",
                              description="Below are the exact Steamy commands you can use in-channel :",
                              color=discord.Colour.blue())
        embed.set_thumbnail(url="https://imgur.com/KtPxVZS.jpeg")
        embed.add_field(name='$rarest_achievement "GAME NAME"',
                        value='Prints the least unlocked achievement for a given game', inline=False)
        embed.add_field(name='$users_game_playtime "USER NAME" "GAME NAME"',
                        value='Prints a given user\'s played hours on a given game', inline=False)
        embed.add_field(name='$users_total_playtime "USER NAME"',
                        value='Prints a given user\'s total played hours on Steam', inline=False)
        embed.add_field(name='$game_player_count "GAME NAME"',
                        value='Prints the current player count for a given game', inline=False)
        await ctx.message.author.send(embed=embed)
        await ctx.send('A guide on commands for Steamy has been sent to you in a private message.')

    @bot.command(
        name="game_id", description="Prints the ID for a given game"
    )
    async def game_id(ctx, arg: str):
        try:
            await ctx.send(bot_helper.get_game_id(arg))
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="user_id", description="Prints the ID for a given user"
    )
    async def user_id(ctx, arg: str):
        try:
            await ctx.send(bot_helper.get_user_id(arg))
        except UserIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="rarest_achievement", description="Prints the least unlocked achievement for a given game"
    )
    async def rarest_achievement(ctx, arg: str):
        rarest_achievement_strings = bot_helper.rarest_achievement_desc(arg)
        embed = discord.Embed(title=f"{rarest_achievement_strings.name}",
                              description=f"{rarest_achievement_strings.achievement}\n\n"
                                          f"{rarest_achievement_strings.description}",
                              color=discord.Colour.blue())
        embed.set_thumbnail(url=f"{rarest_achievement_strings.icon}")
        try:
            await ctx.send(embed=embed)
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="users_game_playtime", description="Prints a given user's played hours on a given game"
    )
    async def users_game_playtime(ctx, arg1: str, arg2: str):
        playtime = bot_helper.users_game_playtime_desc(arg1, arg2)
        embed = discord.Embed(title=f"{playtime.name}",
                              description=f"{playtime.description}",
                              color=discord.Colour.blue())
        embed.set_thumbnail(url=f"{playtime.icon}")
        try:
            await ctx.send(embed=embed)
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="users_total_playtime", description="Prints a given user's total played hours on Steam"
    )
    async def users_total_playtime(ctx, arg: str):
        try:
            await ctx.send(bot_helper.users_total_playtime_desc(arg))
        except (GameIsNoneError, UserIsNoneError) as exc:
            await ctx.send(exc)

    @bot.command(
        name="game_player_count", description="Prints the current player count for a given game"
    )
    async def game_player_count(ctx, arg: str):
        try:
            await ctx.send(bot_helper.game_player_count_desc(arg))
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command()
    async def all_game_player_count(ctx):
        await ctx.send(steam_api.get_all_game_player_counts())

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Oops! You didn't include an argument with the command")
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
