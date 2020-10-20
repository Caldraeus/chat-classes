import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

class cultist(commands.Cog): # self.qualified_name
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    async def pray(self, ctx): # Costs 2 ap
        if self.bot.users_classes[str(ctx.author.id)] == "cultist goon":
            ap_works = await h.alter_ap(ctx.message, 2, self.bot)
            if ap_works:
                await ctx.send("Epic")
    
            


# A setup function the every cog has
def setup(bot):
    bot.add_cog(cultist(bot))
