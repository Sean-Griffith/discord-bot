import discord
import datetime

def generate_ge_embed(item_name, item_data):
        # Embed base intialization
        item_embed = discord.Embed(description="")
        # Set embed thumnail to user profile picture
        item_embed.set_thumbnail(url="https://services.runescape.com/m=itemdb_rs/obj_sprite.gif?id={}".format(item_data["id"]))
        # Set title, include username and link to their profile + icon for their country
        item_embed.set_author(name=str(item_name))

        # Add detailed statistics to embed
        item_cost = format(item_data["price"], ",")
        item_embed.add_field(name="__**Cost**__",value=item_cost, inline=False)
        item_embed.set_image(url="https://services.runescape.com/m=itemdb_rs/api/graph/{}.json".format(item_data["id"]))

        return item_embed

def generated_tms_embed(tms_data, tms_date):
        # Embed base intialization
        tms_embed = discord.Embed(description="")

        # Set title/author
        tms_embed.set_author(name="Traveling Merchant Stock for {}/{}/{}".format(tms_date.month,
                                                                                 tms_date.day,
                                                                                 tms_date.year))
 
        # Set merchant stock values
        tms_embed.add_field(name="Item 1", value=str(tms_data[1]), inline=True)
        tms_embed.add_field(name="Item 2", value=str(tms_data[2]), inline=True)
        tms_embed.add_field(name="Item 3", value=str(tms_data[3]), inline=True)

        return tms_embed