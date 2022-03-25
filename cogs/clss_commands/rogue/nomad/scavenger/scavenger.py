import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
from asyncio import TimeoutError
import aiosqlite

class scavenger(commands.Cog): # It is worth noting that this class has a lot to do with the shop command, found in economy.py.
    def __init__(self, bot):
        self.bot = bot
        self.scrap_items = [
            "boom bot", # Randomly explodes on someone after a period of time.
            "gold spitter", # Spits gold out at the scavenger randomly.
            "goober gobber", # Gives a status effect to someone you target
            "fredster", # It's Fredster! He's so cool. Inspires you!
            "scrapbot", # Spits out some scrap
            "yoinker" # Steals an item.
        ]

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def tinker(self, ctx): # Open a trade menu with someone.
        if self.bot.users_classes[str(ctx.author.id)] == "scavenger":
            if await h.remove_items(ctx.author.id, self.bot, "scrap", 5, True):
                random.shuffle(self.scrap_items)
                chosen_item = random.choice(self.scrap_items)
                await ctx.send(f"🔧 | You tinker with your scrap and create a... **{chosen_item.title()}**! You put it in your inventory.")
                await h.alter_items(ctx.author.id, ctx, self.bot, chosen_item, 1)
            else:
                await ctx.send("🔧 | You don't have enough scrap for this! You need 5 total!")

# A setup function the every cog has
def setup(bot):
    bot.add_cog(scavenger(bot)) 