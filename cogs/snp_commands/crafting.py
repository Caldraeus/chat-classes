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
from asyncio.exceptions import TimeoutError
import sqlite3
from datetime import datetime
import json

class crafting(commands.Cog): #TODO: Implement faction race commands, and the ability to set faction requirements.
    def __init__(self, bot):
        self.bot = bot
        with open('cogs/snp_commands/materials.json') as f:
            self.materials_data = json.load(f)
        
    pass

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

    pass # EOF
        
    @commands.command(aliases=["cat"])
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    async def catalogue(self, ctx, *, material_name: str):
        material_name = material_name.lower()
        mats = list(list(zip(*self.materials_data))[0])
        if material_name in mats:
            mat_index = mats.index(material_name)
            wanted_material = self.materials_data[mat_index]
            wanted_material = wanted_material[material_name]
            profile = discord.Embed(title=f"{material_name.title()} Information", colour=discord.Colour(0x40c9ff), description=wanted_material['description'])
            profile.set_thumbnail(url=wanted_material['image_link'])
            profile.set_footer(text=f"Rarity: {wanted_material['rarity']}", icon_url="")
            profile.add_field(name="Base Sell Price", value=f"{wanted_material['sells_for']} G", inline=True)
            profile.add_field(name="Item Type", value=wanted_material['type'], inline=True)
            await ctx.send(embed=profile)
        else:
            await ctx.send("Invalid material name! Did you make a typo?")

    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    @is_in_chan(802622567642693653)
    async def craft(self, ctx, amount: int, *, item):
        pass # await update_materials(ctx.author.id, ["coal", material], [-smelting_cost, -amount], ctx)         

class MaterialError(Exception):
    pass

async def update_materials(uid, material, amount_added, chan = None):
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
    bot.add_cog(crafting(bot))
