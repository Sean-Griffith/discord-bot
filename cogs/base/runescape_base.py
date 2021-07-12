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

def generated_tms_embed(tms_data, tms_date, query=None):
        # Embed base intialization
        tms_embed = discord.Embed(description="")

        # Set title/author
        if(query == None and len(tms_data) == 1 and len(tms_data[0]) == 4):
                tms_embed.set_author(name="Traveling Merchant Stock for {}/{}/{}".format(tms_date[0].month,
                                                                                         tms_date[0].day,
                                                                                         tms_date[0].year))
                # Set merchant stock values
                tms_embed.add_field(name="Item 1", value=str(tms_data[0][1]), inline=True)
                tms_embed.add_field(name="Item 2", value=str(tms_data[0][2]), inline=True)
                tms_embed.add_field(name="Item 3", value=str(tms_data[0][3]), inline=True)
        else:
                tms_embed.set_author(name="Dates for next three occurances of {}".format(query))
                # Set merchant stock values for each date
                
                for i in range(0,len(tms_date)):
                        value_str = ""
                        for j in range(1, len(tms_data[i])):
                                if(str(tms_data[i][j]).lower() == str(query).lower()):
                                        value_str += "**{}**\n".format(tms_data[i][j])
                                else:
                                        value_str += "{}\n".format(tms_data[i][j])
                                
                        tms_embed.add_field(name="{}/{}/{}".format(tms_date[i].month, tms_date[i].day, tms_date[i].year), 
                                            value=value_str)
        

        return tms_embed