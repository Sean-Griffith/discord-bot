import discord
from discord.ext import tasks, commands
import asyncio
import os
import bot_setup


bot = None

try:
    # Load settings
    bot_setup.generate_files()
    bot, bot_token = bot_setup.define_settings()
    bot_setup.setup_tasks(bot)
    
    # Load modules/cogs with additional functionality for the bot before running
    bot_setup.load_cogs(bot)
    if(bot_token):
        bot.run(bot_token)
    else:
        print("Invalid token input. Add bot token to environment variables before launching.")
except Exception as e:
    print(e)
    bot.close()
    raise e