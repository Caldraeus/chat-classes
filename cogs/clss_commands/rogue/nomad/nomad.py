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
        keys = list(cog.nomad_homes.keys()) # protector = keys[vals.index(target)]
        vals = list(cog.nomad_homes.values())
        try:
            mss = f"**{ctx.channel.name.title()}** is the home of **{keys[vals.index(ctx.channel)].display_name}**!"
            if ctx.author in keys:
                if cog.nomad_homes[ctx.author] == ctx.channel:
                    mss += "\n\nThis is your home!"
                else:
                    mss += f"\n\nYour home is **{cog.nomad_homes[ctx.author].name.title()}** in **{cog.nomad_homes[ctx.author].guild.name}**"
            else:
                mss += "\n\nYou have no home!"
            
            await ctx.send(mss)
        except ValueError:
            mss = "No Nomad has claimed this channel as their home!"
            if ctx.author in keys:
                if cog.nomad_homes[ctx.author] == ctx.channel:
                    mss += "\n\nThis is your home!"
                else:
                    mss += f"\n\nYour home is **{cog.nomad_homes[ctx.author].name.title()}** in **{cog.nomad_homes[ctx.author].guild.name}**"
            await ctx.send(mss)

                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(nomad(bot)) 