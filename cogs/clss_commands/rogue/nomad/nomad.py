import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
from asyncio import TimeoutError
import aiosqlite

class nomad(commands.Cog): # It is worth noting that this class has a lot to do with the shop command, found in economy.py.
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def home(self, ctx): # Show who's home the current channel is.
        cog = self.bot.get_cog('rogue')
        await ctx.send(cog.nomad_homes)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(nomad(bot)) 