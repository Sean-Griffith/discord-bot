import os

def load_cogs(bot):
# Load Cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # Attempt to load the extension
            try:
                bot.load_extension("cogs.{}".format(filename[:-3]))
                print("Loaded cog: [{}]".format(filename[:-3]))
            except Exception as error:
                print("{} could not be loaded. [{}]".format(filename[:-3], error))