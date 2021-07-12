import discord
from discord.ext import commands
import datetime
import requests
import json
from .base import runescape_base as RB

class Runescape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rswiki_session = requests.Session()
        self.rswiki_session.headers["User-Agent"] = "Discord bot for querying grand exchange data."

    @commands.command(aliases = ["ge"])
    async def grand_exchange(self, ctx, *item_name):
        item_name = " ".join(item_name)
        print("Search for:", item_name)

        # Query rswiki for GE data
        url = "https://api.weirdgloop.org/exchange/history/rs/latest"
        
        data = self.rswiki_session.get(url+"?name={}".format(item_name))

        item_name = list(data.json().keys())[0]
        item_data = data.json()[item_name]

        await ctx.channel.send(embed=RB.generate_ge_embed(item_name, item_data))

    @commands.command(aliases = ["tms"])
    async def traveling_merchant(self, ctx, option=None, *query):
        
        query_fixed = None
        if(query and len(query) > 0):
            query = str("_".join(query))
            query_fixed = query.replace("_"," ").capitalize()
            print("Querying for:",query)

        tms_date = []
        tms_data = []

        if(option == None):
            # Query rswiki for todays Traveling Merchant Stock
            url = "https://api.weirdgloop.org/runescape/tms/current"

            # Get todays stock
            tms_data.append(self.rswiki_session.get(url).json())
            tms_date.append(datetime.date.today())

        elif(option == "2"):
            # Query rswiki for tomorrows Traveling Merchant Stock
            url = "https://api.weirdgloop.org/runescape/tms/next"
            # Get tommorrows stock
            tms_data.append(self.rswiki_session.get(url).json())

            # Get tomorrows date
            tms_date.append(datetime.date.today())
            tms_date[0] += datetime.timedelta(days=1)
            
        elif(option == "3"):

            # Query rswiki to search for next appearance of query in Traveling Merchant Stock
            url = "https://api.weirdgloop.org/runescape/tms/search?name={}".format(query_fixed)
            
            # Submit query
            tms_data = self.rswiki_session.get(url).json()
            
            # Get first occurance of queried item in stock if the query was successful
            if(isinstance(tms_data, list) and len(tms_data) > 0):
                multi_tms_data = []

                for i in range(0,len(tms_data)):
                    daily_stock = tms_data[i]["items"]

                    multi_tms_data.append(daily_stock)
                    tms_date.append(datetime.datetime.strptime(tms_data[i]['date'], "%d %B %Y"))
                
                tms_data = multi_tms_data
        
        if(type(tms_data) == list):
            await ctx.send(embed=RB.generated_tms_embed(tms_data, tms_date, query_fixed))
        else:
            await ctx.send("Could not find specified stock.")

def setup(bot):
    bot.add_cog(Runescape(bot))