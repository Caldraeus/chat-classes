import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class trader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def trade(self, ctx, target: discord.Member = None): # Open a trade menu with someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "trader":
                if (str(target.id) in list(self.bot.registered_users.keys())):
                    await ctx.send("Valid trade target")
                else:
                    await ctx.send("Invalid trading target! You must target a user registered in the bot.")
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(trader(bot)) 

"""
chosen = await self.bot.wait_for('message', check=check, timeout=360)
chosen = chosen.content.lower()


def check(m: discord.Message):
    return m.content and m.channel == ctx.message.channel and m.author.id == ctx.author.id
"""