import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    
    @commands.command()
    @commands.guild_only()
    async def quest(self, ctx):
        if str(ctx.author.id) in self.bot.registered_users:
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select completed_quests, currently_questing from users where id = '{ctx.author.id}';") as chan:
                    quest = await chan.fetchone()
                    if quest:
                        if quest[1] != 0: # If the user has a quest...
                            quest_id = quest[1] # Setting this as a variable to close the first connection.
                if quest and quest[1] != 0 and quest[1] != 18:
                    async with conn.execute(f"select * from quests where quest_id = {quest_id}") as q_info:
                        quest_info = await q_info.fetchone()
                        questers = quest_info[5].split("|")
                        for guy in questers:
                            new_guy = guy.split(",")
                            questers[questers.index(guy)] = new_guy # I don't want to comment this and I know I will regret this. 
                    for people in questers:
                        if people[0] == str(ctx.author.id):
                            progress = people[1]
                    
                    try:
                        embed = discord.Embed(title=f"Quest: {quest_info[6]}", colour=discord.Colour.from_rgb(255,192,203), description=f'*{quest_info[1]}*\nProgress: {progress} / {quest_info[7]}')
                        embed.set_footer(text=f"Reward: {quest_info[2].title()} ({quest_info[3]})", icon_url="")
                        embed.set_thumbnail(url=quest_info[4])
                        await ctx.send(content=ctx.author.mention, embed=embed)
                    except UnboundLocalError: # This is a weird error thing. If this keeps having I'll need to figure something out.
                        print("If you're seeing this error message, you've fucked up")
                        await ctx.send("Something broke! Message the bot creator immediately! Caldraeus#1337")
                elif quest and quest[1] != 0 and quest[1] == 18:
                    async with conn.execute(f"select * from quests where quest_id = {quest_id}") as q_info:
                        quest_info = await q_info.fetchone()
                        questers = quest_info[5].split("|")
                    for people in questers:
                        people = people.split(",")
                        if people[0] == str(ctx.author.id):
                            progress = "Waiting"
                    
                    try:
                        embed = discord.Embed(title=f"{quest_info[6]}", colour=discord.Colour.from_rgb(0,0,0), description=f'*{quest_info[1]}*\nProgress: ΛƜΛɪŤɪЛƓϤØЦ尺らØЦŁ')
                        embed.set_footer(text=f"Reward: ᛞᛖᚨᛏᚺᛞᛖᚨᛏᚺᛞᛖᚨᛏᚺᛞᛖᚨᛏᚺ", icon_url="")
                        embed.set_thumbnail(url=quest_info[4])
                        await ctx.send(content=ctx.author.mention, embed=embed)
                    except SyntaxError: # This is a weird error thing. If this keeps having I'll need to figure something out.
                        print("If you're seeing this error message, you've fucked up")
                        await ctx.send("Something broke! Message the bot creator immediately! Caldraeus#1337")

                else:
                    await ctx.send("You currently do not have a quest! Get one by being active in chat!")
    
    @commands.command()
    @commands.guild_only()
    async def abandon(self, ctx):
        try:
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select currently_questing from users where id = '{ctx.author.id}';") as chan:
                    quest = await chan.fetchone()
            if quest:
                quest = quest[0]
                await h.update_quest(ctx.message, quest, -1, self.bot)
        except TypeError:
            await ctx.send("You have no active quest!")

# A setup function the every cog has
def setup(bot):
    bot.add_cog(quests(bot))
