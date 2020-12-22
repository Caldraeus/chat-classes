import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class owner_only(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def servers(self, ctx): # Just displays the amount of servers it is in... 75 here we come!
        await ctx.send(len(self.bot.guilds))

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def say(self, ctx, *, stuff): 
        await ctx.message.delete()
        await ctx.send(stuff)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def fquest(self, ctx, target: discord.User = None):
        if target: # message, bot, uid=None, override=False
            await h.fetch_random_quest(ctx.message, self.bot, target, override=True)
        else:
            await h.fetch_random_quest(ctx.message, self.bot, override=True)
    
    @commands.command()
    @commands.is_owner()
    async def release(self, ctx, version, *, notes):
        channel = self.bot.get_channel(734108098129821757)
        embed = discord.Embed(title=f"❗ Version {version} Released! ❗", colour=discord.Colour.from_rgb(255,0,0), description=notes)
        mss = await channel.send(content="╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲\n\n<@&738883975954563132>\n\n", embed=embed)
        await mss.publish()

    @commands.command()
    @commands.is_owner()
    async def alterclass(self, ctx, *, class_name):
        class_name = class_name.lower()
        async with aiosqlite.connect('main.db') as conn:
            await conn.execute(f"update users set class = '{class_name}' where id = '{ctx.author.id}'")
            await conn.commit()
        self.bot.users_classes[str(ctx.author.id)] = class_name
        await ctx.send("✅ | Class has been altered with [0] issues.")

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, target: discord.User, effect, amount: int):
        await h.add_effect(target, self.bot, effect.lower(), amount)
        await ctx.send(f"Applied {amount} stacks of {effect} to user.")

    @commands.command()
    @commands.is_owner()
    async def setcoolness(self, ctx, target: discord.User, coolness):
        async with aiosqlite.connect('main.db') as conn:
            await conn.execute(f"update users set coolness = {coolness} where id = '{target.id}'")
            await conn.commit()
        await ctx.send("✅ | Targets coolness has been altered with [0] errors.")

# A setup function the every cog has
def setup(bot):
    bot.add_cog(owner_only(bot))
