import discord
from discord.ext import tasks, commands
import asyncio
import os

def define_settings():
    bot_token = ""
    if("bot_token" in os.environ):
        bot_token = os.environ["bot_token"]

    # Set the command prefix for users trying to interact with the bot
    bot = commands.Bot(command_prefix="?", case_insensitive=True)

    # Remove default help command for custom implementation
    bot.remove_command("help")

    return bot, bot_token

def load_cogs(bot):
# Load Cogs
    for filename in os.listdir("./cogs"):
        if (filename.endswith(".py") and not filename.startswith("__")):
            # Attempt to load the extension
            try:
                bot.load_extension("cogs.{}".format(filename[:-3]))
                print("Loaded cog: [{}]".format(filename[:-3]))
            except Exception as error:
                print("{} could not be loaded. [{}]".format(filename[:-3], error))