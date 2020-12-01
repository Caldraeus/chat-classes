import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = {
            "coffee" : 50,
            "monster" : 150,
            "adrenaline" : 250,
        }

        self.hidden_items = {
            "demon cookie" : 500
        }

    @commands.command()
    @commands.guild_only()
    async def shop(self, ctx, page = "consumables", number = 1):
        if page == "consumables" and number == 1:
            embed = discord.Embed(title=f"🍺 Consumables Shop 🍺", colour=discord.Colour.from_rgb(166, 148, 255))
            # embed.set_footer(text=f"Use {h.prefix}shop {page} page_number to see more!")
            embed.set_thumbnail(url="https://img.icons8.com/cotton/2x/shop--v3.png")
            embed.add_field(name=f"Coffee | {self.items.get('coffee')} G", value=f'A quick boost. Delicious and refreshing! Restores 2 AP.', inline=False)
            embed.add_field(name=f"Monster | {self.items.get('monster')} G", value=f'A monster energy. Great if you ignore the kidney stones! Restores 6 AP.', inline=False)
            embed.add_field(name=f"Adrenaline | {self.items.get('adrenaline')} G", value="A pure vial of adrenaline. Very strong. Restores 10 AP.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def use(self, ctx, *, item: str = None):
        if item:
            item = item.lower()
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select inventory, gold from users where id = '{ctx.author.id}'") as u_info:
                    user_info = await u_info.fetchone()

            inv = user_info[0].split("|")
            gold = user_info[1]
            
            for owned_item in inv:
                new_guy = owned_item.split(",")
                inv[inv.index(owned_item)] = new_guy
            
            end = ""
            
            if [''] in inv:
                inv.remove(['']) # Temporary workaround.
            items = [item[0] for item in inv] # Array of just the names of the items in the 2D array.

            if item in self.items or item in self.hidden_items:
                if item in items:
                    if ctx.author.id in self.bot.server_boosters:
                        max_ap = 40
                    else:
                        max_ap = 20
                    #### Item handling. This, unfortunately, is going to be a very long if statement mess. Since I plan to add a large variety of items, with many different effects, it has to be this way.
                    ####
                    if item == "coffee":
                        await ctx.send("☕ | You drink your coffee... it's delicious! Now you have a bit more energy. (+2 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 2
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "monster":
                        await ctx.send("<:monster:739176788629913739> | You drink your monster energy... it's energizing! Now you have a bit more energy. (+6 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 6
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "adrenaline":
                        await ctx.send("💉 | You inject a vial of pure adrenaline... WOOO! **NOW YOU HAVE A LOT MORE ENERGY!**. (+10 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 10
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "demon cookie":
                        await ctx.send("🍪 | You munch on Lord Greymuul's homemade chocolate chip cookies... Wait a minute, these are raisins! How demonic! You're filled with rage. (+20 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 20
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap

                                
                    ####
                    ####
                    index = items.index(item)
                    
                    new_amount = int(inv[index][1]) - 1
                    
                    if new_amount > 0:
                        inv[index][1] = str(new_amount)
                        for sublist in inv:
                            if inv.index(sublist) == len(inv)-1:
                                end += f"{','.join(sublist)}"
                            else:
                                end += f"{','.join(sublist)}|"
                    else:
                        for sublist in inv:
                            if sublist[0] != item:
                                if inv.index(sublist) == len(inv)-1:
                                    end += f"{','.join(sublist)}"
                                else:
                                    end += f"{','.join(sublist)}|"


                    async with aiosqlite.connect('main.db') as conn:
                        await conn.execute(f"update users set inventory = '{end}' where id = '{ctx.author.id}';")
                        await conn.commit()
                else:
                    await ctx.send(f"You are not currently in posession of {item.title()}. Perhaps you made a typo?")
               
    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, *, item: str = None):
        if item:
            if item in self.items:
                await h.alter_items(ctx.author.id, ctx, self.bot, item.lower(), 1, self.items[item.lower()])
            else:
                await ctx.send("That item doesn't exist. Did you make a typo?")
            
        else:
            await ctx.send("You forgot to specify what you'd like to buy!")

        

# A setup function the every cog has
def setup(bot):
    bot.add_cog(shop(bot))
