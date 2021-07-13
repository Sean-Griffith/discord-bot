import discord
from discord.ext import tasks, commands
import asyncio
import os
import requests
import datetime
import cogs.base.runescape_base as RB

def setup_tasks(bot):
    bot.loop.create_task(check_tms_reminders(bot))

async def check_tms_reminders(bot):
    await bot.wait_until_ready()
    
    while bot.is_ready:

        tms_date = datetime.datetime.utcnow()

        with open("cogs/base/data/tms_reminder_last.txt") as last_reminder_file:
            last_reminder = last_reminder_file.readline().strip()
            last_reminder_date = None
            if(len(last_reminder) > 2):
                last_reminder_date = datetime.datetime.strptime(last_reminder, "%Y-%m-%d %H:%M:%S")
                time_since_reminder = tms_date - last_reminder_date
                print("time since last reminder:", time_since_reminder)
                if(time_since_reminder.days < 1):
                    sleep_time = datetime.timedelta(days=1) - time_since_reminder
                    print("Sleeping reminders for:", sleep_time.seconds)
                    await asyncio.sleep(sleep_time.seconds)

        # Query rswiki for todays Traveling Merchant Stock
        url = "https://api.weirdgloop.org/runescape/tms/current"

        # Get todays stock
        reminder_session = requests.Session()
        reminder_session.headers["User-Agent"] = "Discord bot for daily traveling merchant stock reminders."
        tms_data = reminder_session.get(url).json()

        tmsr_embed = RB.generate_tms_embed([tms_data], [tms_date])

        tms_reminders = []
        with open("cogs/base/data/tms_reminders.txt") as tms_reminders_file:
            tms_reminders = tms_reminders_file.readlines()

        reminder_list_str = ""
        for reminder in tms_reminders:
            split_reminder = reminder.rstrip().split(" ")
            uid = split_reminder[0].strip()
            for item in split_reminder[1:]:
                if(item.rstrip().replace("_"," ") in tms_data):
                    reminder_list_str += "<@!{}>\n".format(uid)
        
        with open("cogs/base/data/tms_reminder_cid.txt") as channel_id_file:
            cid = channel_id_file.readline().rstrip()

        if(cid and len(reminder_list_str) > 0):
            channel = bot.get_channel(id=int(cid))
            await channel.send("**TMS Reminder**\n"+reminder_list_str)
            await channel.send(embed=tmsr_embed)

        with open("cogs/base/data/tms_reminder_last.txt", "w") as last_reminder_file:
            ct = datetime.datetime.utcnow()
            last_reminder_file.write("{}-{}-{} {}:{}:{}".format(ct.year, ct.month, ct.day, ct.hour, ct.minute, int(ct.second)))

def generate_files():
    with open("cogs/base/data/necessary_files.txt") as necessary_files:
        files = necessary_files.readlines()
    
    for file in files:
        my_file = open(file.strip(), 'a')
        my_file.close()

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