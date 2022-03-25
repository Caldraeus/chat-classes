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
    @commands.is_owner()
    async def update(self, ctx, cog, new = None):
        if new == None:
            lists = self.bot.extensions
            for item in lists:
                item = item.split('.')
                if item[-1] == cog.lower():
                    pwd = '.'.join(item)
                    break

            try:
                self.bot.reload_extension(str(pwd))
                await ctx.send(f"Successfully updated `{pwd}` with [0] errors.")
            except UnboundLocalError:
                await ctx.send(f"❗ | Cog `{cog}` not found.")
        else:
            try:
                self.bot.load_extension(cog)
                await ctx.send(f"Loaded new cog `{cog}`.")
            except ValueError:
                await ctx.send(f"❗ | Invalid path for `{cog}`.")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def servers(self, ctx): # Just displays the amount of servers it is in... 75 here we come!
        await ctx.send(len(self.bot.guilds))

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def testap(self, ctx): # Just displays the amount of servers it is in... 75 here we come!
        self.bot.users_ap[str(ctx.author.id)] = 5000
        await ctx.send("AP reset to 5000 for testing.")

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
    async def givegold(self, ctx, target: discord.User, amount: int):
        await h.add_gold(target.id, amount, self.bot, boost_null=True)
        await ctx.send(f"✅ | Granted {amount} G to user {target.display_name}.")

    @commands.command()
    @commands.is_owner()
    async def setcoolness(self, ctx, target: discord.User, coolness):
        async with aiosqlite.connect('main.db') as conn:
            await conn.execute(f"update users set coolness = {coolness} where id = '{target.id}'")
            await conn.commit()
        await ctx.send("✅ | Targets coolness has been altered with [0] errors.")

    @commands.command()
    @commands.is_owner()
    async def reset(self, ctx):
        await ctx.send("Forcing daily reset. Check console log for errors.")
        self.bot.force_reset = True

    @commands.command()
    @commands.is_owner()
    async def giveitem(self, ctx, target: discord.User, amount: int, *, item_name: str):
        await h.alter_items(target.id, ctx, self.bot, item_name.lower(), amount)
        await ctx.send(f"✅ | Gave {amount} `{item_name.title()}` to **{target.display_name}**")
    
    @commands.command()
    @commands.is_owner()
    async def giveach(self, ctx, target: discord.User, ach_id: int):
        await ctx.send(f"Attempting to award achievement to `{target.display_name}`.")
        await h.award_ach(ach_id, ctx.channel, target, self.bot, False)

# A setup function the every cog has
def setup(bot):
    bot.add_cog(owner_only(bot))
