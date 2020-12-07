import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command(aliases=["code"])
    @commands.guild_only()
    async def coding(self, ctx):
        await h.award_ach(9, ctx.message, self.bot)
        await ctx.message.delete()
        embed = discord.Embed(title="", colour=discord.Colour(0x2dc3e1), description="")

        embed.set_image(url="https://i.redd.it/mtkfcgtzdu041.jpg")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def whom(self, ctx):
        await h.award_ach(9, ctx.message, self.bot)
        await ctx.message.delete()
        await ctx.send("https://youtu.be/UNPP0IND5u8")

    @commands.command()
    @commands.guild_only()
    async def god(self, ctx):
        await h.award_ach(9, ctx.message, self.bot)
        await ctx.message.delete()
        embed = discord.Embed(title="", colour=discord.Colour(0x2dc3e1), description="")

        embed.set_image(url="https://www.whichwich.com/wp-content/uploads/2017/03/WW-Horizontal-Logo-SUPERIOR-SANDWICHES_Yellow.png")
        await ctx.send(embed=embed)
               

# A setup function the every cog has
def setup(bot):
    bot.add_cog(secret(bot))
