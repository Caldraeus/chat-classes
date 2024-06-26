import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def safezone(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select bchannels from servers where id = '{ctx.guild.id}'") as g:
                banned = await g.fetchone()
                banned = banned[0]
                banned = banned.split('|')
                if str(channel.id) not in banned: # This is redundant. But I'm keeping it here JUST IN CASE.
                    banned.append(str(channel.id))
                    self.bot.banned_channels.append(str(channel.id))
                    final = '|'.join(banned)
                    await conn.execute(f"update servers set bchannels = '{final}' where id = '{ctx.guild.id}'")
                    await conn.commit()
                    await ctx.message.add_reaction('✅')
                else: # See above comment.
                    await ctx.send("Channel is already disabled!")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def classzone(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select bchannels from servers where id = '{ctx.guild.id}'") as g:
                banned = await g.fetchone()
                banned = banned[0]
                banned = banned.split('|')
                if str(channel.id) in banned: # This is redundant. But I'm keeping it here JUST IN CASE.
                    banned.pop(banned.index(str(channel.id)))
                    self.bot.banned_channels.remove(str(channel.id))
                    final = '|'.join(banned)
                    await conn.execute(f"update servers set bchannels = '{final}' where id = '{ctx.guild.id}'")
                    await conn.commit()
                    await ctx.message.add_reaction('✅')
                else: # See above comment.
                    await ctx.send("Channel is already enabled!")

    @commands.command()
    @commands.guild_only()
    async def disclaimer(self, ctx):
        guild = ctx.guild
        await ctx.send(f"Greetings, members of {guild.name}! Before this bot is active, the owner must understand that this bot messes with chat quite a bit. This includes sending messages, deleting messages, and creating (temporary!) channels. This bot will not destroy your server, I promise. I would only recommend this bot for small servers with friends/etc. For more information on managing this bot and what it does, use `;help` and read on how to disable the bot in specific channels.\n\nNow that that is all said and done, I will need the server owner ({guild.owner.mention}) to say `{h.prefix}enablecc`\n\nAdditionally, this bot makes use of nickname permissions, and it needs the highest role in a guild to operate. If you do not feel comfortable doing this, I understand, but you should recognise that this bot will have less functionality.\n\nThat is all!")

    @commands.command()
    @commands.guild_only()
    async def about(self, ctx):
        profile = discord.Embed(title=f"Chat Classes About", colour=discord.Colour(0x6eaf0b), description="")
        ###
        ###
        profile.set_footer(text=f"Bot Latency: {math.ceil(round(self.bot.latency * 1000, 1))} ms", icon_url="")
        profile.add_field(name="Bot Version", value=self.bot.version, inline=False)
        profile.add_field(name="Creator", value=f'Caldraeus#1337', inline=False)
        profile.add_field(name="Library", value=f'PyCord, a Discord.py Fork', inline=False)
        profile.add_field(name="Extra", value=f'Thank you to everyone who has helped me create this bot! I would also like to thank Kingdom of Loathing for the inspiration to create this bot in the first place. And thank you for using it!', inline=False)
    
    
        await ctx.send(embed=profile)

# A setup function the every cog has
def setup(bot):
    bot.add_cog(management(bot))
