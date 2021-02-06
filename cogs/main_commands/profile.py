import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import time
import aiosqlite
from jishaku.functools import executor_function
from io import BytesIO

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    async def profile(self, ctx, user: discord.Member = None):
        try:
            if user:
                await ctx.send(embed=await h.genprof(user, self.bot.users_ap, self.bot))
            else:
                await ctx.send(embed=await h.genprof(ctx.author, self.bot.users_ap, self.bot))
        except TypeError:
            await ctx.send("User does not have a profile! Run `;start` to get one!")

    @commands.command()
    @commands.guild_only()
    async def effects(self, ctx, target: discord.Member = None):
        if target != None:
            usr = target
        else:
            usr = ctx.author
        effects = self.bot.user_status[usr.id]
        if effects != []:
            profile = discord.Embed(title=f"{usr.display_name}'s Status Effects", colour=discord.Colour.from_rgb(255,105,180))
            for effect in effects:
                profile.add_field(name=f"{effect[0].title()} - {effect[1]}×", value=h.effect_list[effect[0]], inline=False)

            await ctx.send(embed=profile)
        else:
            await ctx.send("No current status effects!")

    @commands.command(aliases=["inv"])
    @commands.guild_only()
    async def inventory(self, ctx):
        # embed.set_author(name="author name", url="https://discordapp.com", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        if str(ctx.author.id) in self.bot.registered_users:
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select inventory, gold from users where id = '{ctx.author.id}'") as u_info:
                    user_info = await u_info.fetchone()

            inv = user_info[0].split("|")
            gold = user_info[1]
            
            for owned_item in inv:
                new_guy = owned_item.split(",")
                inv[inv.index(owned_item)] = new_guy
            
            final_list = ""
            num = 1
            for item in inv:
                if item != ['']:
                    final_list += f"{num}. **{item[0].title()}** × {item[1]}\n\n"
                    num += 1
            
            profile = discord.Embed(title=f"{ctx.author.display_name}'s Inventory", colour=discord.Colour.from_rgb(255,223,0), description=final_list)
            profile.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.send(embed=profile)
            
    # Leaderboard command... it's sorta a profile command!
    @commands.command(aliases=['top'])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        async with aiosqlite.connect('main.db') as con:
            async with con.execute(f"select * from users order by coolness desc;") as lb: # Get their coolness rank!
                stuff = await lb.fetchall()
        final = ""
        in_top = False
        i = 0
        timeout = time.time() + 5   # 25 seconds from now
        total = 5
        amount_skipped = 0 # There's a lot of mumbo jumbo here. Basically, if someone isn't in a server with Chat Classes, we can't find them! So basically, we need to skip over them and get the next guy, so we have to increase the limit by one, the person we're on by one, and count how many we skip so we can make sure the ranks show up normally.
        while i < total:
            if time.time() > timeout:
                await ctx.send("Timeout error.")
                print("------------TIMEOUT ERROR ON TOP------------")
                break
            
            
            user = self.bot.get_user(int(stuff[i][0]))
            if user != None and user.id is not ctx.message.author.id:
                final+=f"#{i+1 - amount_skipped} - {user.name} - {stuff[i][5]} Coolness\n\n"
                i += 1
            elif user != None and user.id is ctx.message.author.id:
                final+=f"**#{i+1 - amount_skipped} - {user.name} - {stuff[i][5]} Coolness**\n\n"
                in_top = True
                if i+1 == 1:
                    await h.award_ach(13, ctx.message, self.bot)
                    await h.award_ach(12, ctx.message, self.bot)
                else:
                    await h.award_ach(12, ctx.message, self.bot)
                i += 1
            elif user == None:
                i += 1
                total += 1
                amount_skipped += 1
                continue

        if user != None:
            if not in_top:
                rank = 1 
                coolness = 0
                for usr in stuff:
                    if usr[0] == str(ctx.message.author.id):
                        coolness = usr[5]
                        break
                    else:
                        rank+=1

                final+=f"**.  .  .\n\n#{rank} - {ctx.message.author.name} - {coolness}**"
        
        profile = discord.Embed(title=f"👑 𝒯𝒽𝑒 𝒞𝑜𝑜𝓁𝑒𝓈𝓉 𝒦𝒾𝒹𝓈 👑", colour=discord.Colour.from_rgb(255,255,0), description=final)
        profile.set_thumbnail(url="https://cdn.discordapp.com/attachments/491359456337330198/733460129785184297/Funny-Dog-Wearing-Sunglasses.png")
        
        ###
        
        await ctx.send(embed=profile)

    @commands.command(aliases=["achs"])
    @commands.guild_only()
    async def achievements(self, ctx, target: discord.User = None):
        if target == None:
            target = ctx.author
        uid = str(target.id)
        final_list = ""
        user_ach = len(self.bot.registered_users[uid]) - 1
        for ach_id in self.bot.registered_users[uid]:
            if ach_id > 0:
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from achievements where id = '{ach_id}'") as ach:
                        ach_info = await ach.fetchone()
                        if ach_info[5] != "None":
                            final_list += f"\n**{ach_info[1]}** - Unlocks *{ach_info[5]}*"
                        else:
                            final_list += f"\n**{ach_info[1]}**"
                    async with conn.execute("select count(*) from achievements;") as numcount:
                        num = await numcount.fetchone()
                        num_not = h.unobtainable_achs
                        total_achievements = num[0]-h.unobtainable_achs # Self explanatory. We subtract the amount of "unobtainable" achievements.
                        """
                        Unobtainable Achievements
                        #15 - Beloved By...
                        """
        if final_list != "":
            profile = discord.Embed(title=f"{target.display_name}'s Achievements", colour=discord.Colour.from_rgb(255,69,0), description=final_list)
            profile.set_thumbnail(url=target.avatar_url)
            profile.add_field(name="Total", value=f"{user_ach} of {total_achievements} Unlocked ({int((user_ach/total_achievements)*100)}%)", inline=False)
            await ctx.send(embed=profile)
                    



# A setup function the every cog has
def setup(bot):
    bot.add_cog(profile(bot))
