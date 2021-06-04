import discord
from discord.ext import commands

# (TODO) should be made more secure
def is_it_me(ctx):
    return ctx.author.id == 128320774955073537

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_it_me)
    async def load(self, context, extension):
        try:
            self.bot.load_extension("cogs.{}".format(extension))
            print("Loaded {}".format(extension))
            await context.send("Loaded {}".format(extension))
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))
            raise Exception("custom_err:{} could not be loaded.".format(extension))

    @commands.command()
    @commands.check(is_it_me)
    async def unload(self, context, extension):
        try:
            self.bot.unload_extension("cogs.{}".format(extension))
            print("Unloaded {}".format(extension))
            await context.send("Unloaded {}".format(extension))
        except Exception as error:
            print("{} cannot be unloaded. [{}]".format(extension, error))
            raise Exception("custom_err:{} could not be unloaded.".format(extension))

    @commands.command()
    @commands.check(is_it_me)
    async def reload(self, context, extension):
        try:
            try:
                self.bot.unload_extension("cogs.{}".format(extension))
                print("Unloaded {}".format(extension))
            except Exception as error:
                print("{} cannot be unloaded. [{}]".format(extension, error))
                raise Exception("custom_err:{} could not be unloaded.".format(extension))
            try:
                self.bot.load_extension("cogs.{}".format(extension))
                print("Loaded {}".format(extension))
                await context.send("Reloaded {}".format(extension))
            except Exception as error:
                print("{} cannot be loaded. [{}]".format(extension, error))
                raise
        except:
            raise Exception("custom_err:{} could not be reloaded.".format(extension))

def setup(bot):
    bot.add_cog(Utility(bot))