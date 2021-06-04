import discord
from discord.ext import tasks, commands
import asyncio
import os
from bot_setup import load_cogs

if("bot_token" in os.environ):
    bot_token = os.environ["bot_token"]

#Set the command prefix for users trying to interact with the bot
bot = commands.Bot(command_prefix="?", case_insensitive=True)

try:
    # Load modules/cogs with additional functionality for the bot before running
    load_cogs(bot)
    if(bot_token):
        bot.run(bot_token)
    else:
        print("Invalid token input. Add bot token to environment variables before launching.")
except Exception as e:
    print(e)
    bot.close()
    raise e