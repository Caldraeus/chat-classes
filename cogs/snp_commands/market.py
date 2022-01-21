import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
import asyncio
from discord import Webhook, AsyncWebhookAdapter
from asyncio.exceptions import TimeoutError
import json

class market(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

        with open('cogs/snp_commands/materials.json') as f:
            self.materials_data = json.load(f)

        self.materials = [list(i.keys())[0] for i in self.materials_data]

    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)

    def is_in_cat():
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.category_id == 802594173663314004
        return commands.check(predicate)

    def is_in_chan(chan):
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.id == chan
        return commands.check(predicate)

    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    async def market(self, ctx, *, item: str = None):
        if item != None and item.lower() in self.materials:
            async with aiosqlite.connect('unique.db') as conn: # This should've been in SNP.db but I made an oopsie. No worries, though.
                async with conn.execute(f"SELECT listing_id, listed_cost, stock FROM market_listings WHERE listed_item = '{item.lower()}' limit 10;") as count:
                    listings = await count.fetchall()

            print(listings)
            fstring = "__**💰 Cheapest Listings 💰**__\n\n"
            emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            for i in range(len(listings)):
                current_listing = listings[i]
                fstring += f"{emojis[i]} : `{current_listing[2]}` left, being sold for **{current_listing[1]}** each. (ID: `{current_listing[0]}`)\n\n"
            await ctx.send(fstring)

    @commands.command(aliases=["purchase"])
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    async def marketbuy(self, ctx, mid: int = None, amount: int = None):
        if mid != None and amount != None and amount > 0:
            async with aiosqlite.connect('unique.db') as conn: # This should've been in SNP.db but I made an oopsie. No worries, though.
                async with conn.execute(f"SELECT * FROM market_listings WHERE listing_id = {mid};") as count:
                    listing = await count.fetchone()
            
            if listing == None:
                await ctx.send("That's an invalid listing ID! Double check you have one that's still valid!")
            else:
                print(listing)
                # 1. Update person buying's gold
                # 2. Update person buying's materials
                # 3. Update person selling's gold
                # 4. Update listing, delete if stock hits zero
                # Since we need to check all of these at once, we can't use our premade methods and must check these one by one individually.
                async with aiosqlite.connect('main.db') as conn: # This should've been in SNP.db but I made an oopsie. No worries, though.
                    async with conn.execute(f"SELECT gold FROM users WHERE id = '{ctx.author.id}'") as count:
                        gold = await count.fetchone()
                
                gold = gold[0]
                if not ((gold - listing[3]*amount) < 0) and not (listing[1] == ctx.author.id) and (listing[4] - amount) >= 0:
                    await h.add_gold(ctx.author.id, -listing[3]*amount, self.bot, debt_mode = False, purchase_mode = True, boost_null = False)
                    await update_materials(ctx.author.id, listing[2].lower(), amount)
                    await h.add_gold(listing[1], listing[3]*amount, self.bot, boost_null = True)
                    await ctx.send("<:check_yes:802233343704956968> | Purchase complete!")
                    if (listing[4] - amount) == 0:
                        async with aiosqlite.connect('unique.db') as conn: 
                            await conn.execute(f"DELETE FROM market_listings WHERE listing_id = {mid}")
                            await conn.commit()
                    else:
                        async with aiosqlite.connect('unique.db') as conn: 
                            await conn.execute(f"UPDATE market_listings SET stock = {listing[4] - amount} WHERE listing_id = {mid}")
                            await conn.commit()
                else:
                    await ctx.send("You can't do that! Make sure you double checked everything! (Like the listing's stock, or your gold).")

        
    @commands.command(aliases=["list"])
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    async def lis(self, ctx, amount: int = None, cost: int = None, *, material_name: str):
        def check(m: discord.Message):
            return m.content and m.channel == ctx.message.channel and m.author.id == ctx.author.id
        if amount > 0 and cost and material_name.lower() in self.materials:
            # First, check if they have a current listing and update if so.
            # If no current listing, create one.
            # Make sure to generate a unique ID for each market listing
            async with aiosqlite.connect('unique.db') as conn: # This should've been in SNP.db but I made an oopsie. No worries, though.
                async with conn.execute(f"SELECT listed_cost, stock FROM market_listings WHERE listing_owner = {ctx.author.id} and listed_item = '{material_name.lower()}';") as count:
                    current_amount = await count.fetchall()

            if current_amount == []:
                try:
                    await update_materials(ctx.author.id, material_name.lower(), -amount)
                    await ctx.send(f"Alright! I'll put up a market listing of {amount} **{material_name.title()}**, selling for {cost} each!")
                    async with aiosqlite.connect('unique.db') as conn:
                        await conn.execute(f"insert into market_listings(listing_owner,listed_item,listed_cost,stock) values({ctx.author.id}, '{material_name.lower()}', {cost}, {amount})")
                        await conn.commit()
                except MaterialError:
                    await ctx.send("Woops! Looks like you don't have enough of that material to sell! Try again!")
            else:
                current_stock = current_amount[0][1]
                current_price = current_amount[0][0]
                await ctx.send(f"⚠️ | You already have a listing for **{material_name.title()}**! There's {current_stock} left, being sold for {current_price} each!\n\nDo you wish to update this listing with your new pricing, combining the amounts?")
                chosen = await self.bot.wait_for('message', check=check, timeout=20)
                choice = chosen.content.lower()
                if choice == "yes":
                    try:
                        await update_materials(ctx.author.id, material_name.lower(), -amount)
                        await ctx.send("Alright, I will update your market listing!")
                        async with aiosqlite.connect('unique.db') as conn:
                            await conn.execute(f"update market_listings set listed_cost = {cost}, stock = {current_stock + amount} where listing_owner = {ctx.author.id} AND listed_item = '{material_name.lower()}'")
                            await conn.commit()
                    except MaterialError:
                        await ctx.send("Woops! Looks like you don't have enough of that material to sell! Try again!")
                else:
                    await ctx.send("Alright, creation of a new market listing has been cancelled!")

        else:
            await ctx.send("Looks like you didn't format this properly. Here's an example of how to use the command!\n\n`;list 50 1000 jazzed up mushroom` - *Puts up a listing of 50 jazzed up mushrooms being sold for 1000 each.*") 

class MaterialError(Exception):
    pass


async def update_materials(uid, material, amount_added):
    if type(material) == str:
        material = material.title()
        async with aiosqlite.connect('snp.db') as conn:
            async with conn.execute(f"SELECT amount FROM materials WHERE uid = {uid} and item_name = '{material}';") as count:
                current_amount = await count.fetchall()
        if current_amount == []:
            if amount_added < 0:
                raise MaterialError
            else:
                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"insert into materials values({uid}, '{material}', {amount_added})")
                    await conn.commit()
        else:
            current_amount = current_amount[0][0]
            if current_amount == 0:
                if amount_added < 0:
                    raise MaterialError
                else:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {amount_added} where uid = {uid} and item_name = '{material}'")
                        await conn.commit()
            else:
                if current_amount+amount_added < 0:
                    raise MaterialError
                else:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {current_amount+amount_added} where uid = {uid} and item_name = '{material}'")
                        await conn.commit()
    elif type(material) == list:
        for mat in material: # check if they have enough of each, raise an error if they don't
            index = material.index(mat)
            mat = mat.title()
            
            async with aiosqlite.connect('snp.db') as conn:
                async with conn.execute(f"SELECT amount FROM materials WHERE uid = {uid} and item_name = '{mat}';") as count:
                    current_amount = await count.fetchall()
            if current_amount == []:
                if amount_added[index] < 0:
                    raise MaterialError
            else:
                current_amount = current_amount[0][0]
                if current_amount == 0:
                    if amount_added[index] < 0:
                        raise MaterialError
                else:
                    if current_amount+amount_added[index] < 0:
                        raise MaterialError
        
        for mat in material: # Now apply them
            index = material.index(mat)
            mat = mat.title()
            async with aiosqlite.connect('snp.db') as conn:
                async with conn.execute(f"SELECT amount FROM materials WHERE uid = {uid} and item_name = '{mat}';") as count:
                    current_amount = await count.fetchall()
            if current_amount == []:
                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"insert into materials values({uid}, '{mat}', {amount_added[index]})")
                    await conn.commit()
            else:
                current_amount = current_amount[0][0]
                if current_amount == 0:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {amount_added[index]} where uid = {uid} and item_name = '{mat}'")
                        await conn.commit()
                else:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {current_amount+amount_added[index]} where uid = {uid} and item_name = '{mat}'")
                        await conn.commit()
                    
        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(market(bot))
