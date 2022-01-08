import discord
from discord.ext import commands
import os

import bot_helper
from src.exceptions import GameIsNoneError, UserIsNoneError, ExceedingTopGamesMax, GameHasNoAchievements

DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not DISCORD_BOT_TOKEN:
    raise Exception('No DISCORD_BOT_TOKEN provided')

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')  # Removes discord's built in help command so we can create a custom one


def main():
    @bot.command()
    async def help(ctx):
        embed = discord.Embed(title="Steamy Commands",
                              url="https://github.com/JDGiardino/Steamy/blob/main/README.md",
                              description="Below are the exact Steamy commands you can use in-channel :",
                              color=discord.Colour.blue())
        embed.set_thumbnail(url="https://imgur.com/KtPxVZS.jpeg")
        embed.add_field(name='$achievement GAME NAME',
                        value='Prints the least unlocked achievement for a given game', inline=False)
        embed.add_field(name='$user USER NAME',
                        value='Prints a given user\'s total played hours on Steam', inline=False)
        embed.add_field(name='$game GAME NAME',
                        value='Prints the current player count for a given game', inline=False)
        embed.add_field(name='$top NUMBER',
                        value='Prints the top X played games of a given number up to 100', inline=False)
        embed.add_field(name='$users_game "USER NAME" "GAME NAME"',
                        value='Prints a given user\'s stats on a given game.  \nNOTE: Quotes around the user name '
                              'and game name are required', inline=False)
        await ctx.message.author.send(embed=embed)
        await ctx.send('A guide on commands for Steamy has been sent to you in a private message.')

    @bot.command(
        name="game_id", description="Prints the ID for a given game"
    )
    async def game_id(ctx, *, arg: str):
        try:
            await ctx.send(bot_helper.get_game_id(arg))
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="user_id", description="Prints the ID for a given user"
    )
    async def user_id(ctx, *, arg: str):
        try:
            await ctx.send(bot_helper.get_user_id(arg))
        except UserIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="achievement", description="Prints the least unlocked achievement for a given game"
    )
    async def achievement(ctx, *, arg: str):
        try:
            rarest_achievement = bot_helper.rarest_achievement_desc(arg)
            embed = discord.Embed(title=f"{rarest_achievement.name}",
                                  description=f"{rarest_achievement.achievement}\n\n"
                                              f"{rarest_achievement.description}",
                                  color=discord.Colour.blue())
            embed.set_thumbnail(url=f"{rarest_achievement.icon}")
            await ctx.send(embed=embed)
        except (GameIsNoneError, GameHasNoAchievements) as exc:
            await ctx.send(exc)

    @bot.command(
        name="users_game", description="Prints a given user's stats on a given game"
    )
    async def users_game(ctx, arg1: str, arg2: str):
        try:
            stats = bot_helper.users_game_stats(arg1, arg2)
            embed = discord.Embed(title=f"{stats.name}",
                                  description=f"{stats.description1}\n\n"
                                              f"{stats.description2}",
                                  color=discord.Colour.blue())
            embed.set_thumbnail(url=f"{stats.icon}")
            await ctx.send(embed=embed)
        except (GameIsNoneError, UserIsNoneError) as exc:
            await ctx.send(exc)

    @bot.command(
        name="user", description="Prints a given user's total played hours on Steam"
    )
    async def user(ctx, *, arg: str):
        try:
            stats = bot_helper.users_stats(arg)
            embed = discord.Embed(title=f"{stats.name}",
                                  description=f"{stats.description1}\n\n"
                                              f"{stats.description2}",
                                  color=discord.Colour.blue())
            embed.set_thumbnail(url=f"{stats.icon}")
            await ctx.send(embed=embed)
        except (GameIsNoneError, UserIsNoneError) as exc:
            await ctx.send(exc)

    @bot.command(
        name="game", description="Prints the current player count for a given game"
    )
    async def game(ctx, *, arg: str):
        try:
            stats = bot_helper.game_desc(arg)
            embed = discord.Embed(title=f"{stats.name}",
                                  description=f"{stats.description1}\n\n"
                                              f"{stats.description2}",
                                  color=discord.Colour.blue())
            embed.set_thumbnail(url=f"{stats.icon}")
            await ctx.send(embed=embed)
        except GameIsNoneError as exc:
            await ctx.send(exc)

    @bot.command(
        name="top", description="Prints the top X played games of a given number up to 100"
    )
    async def top(ctx, *, arg: int):
        try:
            stats = bot_helper.get_top_x_games(arg)
            embed = discord.Embed(title=f"{stats.name}",
                                  description=f"{stats.description1}\n\n"
                                              f"{stats.description2}",
                                  color=discord.Colour.blue())
            embed.set_thumbnail(url=f"{stats.icon}")
            await ctx.send(embed=embed)
        except ExceedingTopGamesMax as exc:
            await ctx.send(exc)

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
        elif isinstance(error, GameIsNoneError):
            await ctx.send(error)
        else:
            await ctx.send(f"Ran into an error \"{error}\"  This is unexpected, please report this to the bot creator")

    bot.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
