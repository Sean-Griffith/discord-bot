import discord
from discord.ext import commands 

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # Listen to all messages and log them in console
        if(ctx.author != self.bot.user):
            print(ctx)
            print("{}: {}".format(ctx.author, ctx.content))

def setup(bot):
    bot.add_cog(Core(bot))