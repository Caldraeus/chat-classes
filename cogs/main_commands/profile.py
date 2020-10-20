import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    async def profile(self, ctx, user: discord.Member = None):
        try:
            if user:
                await ctx.send(embed=await h.genprof(user, self.bot.users_ap))
            else:
                await ctx.send(embed=await h.genprof(ctx.author, self.bot.users_ap))
        except TypeError:
            await ctx.send("User does not have a profile! Run `;start` to get one!")

    @commands.command()
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
        for i in range(5):
            user = self.bot.get_user(int(stuff[i][0]))
            if user and user.id is not ctx.message.author.id:
                final+=f"#{i+1} - {user.name} - {stuff[i][5]} Coolness\n\n"
            if user and user.id is ctx.message.author.id:
                final+=f"**#{i+1} - {user.name} - {stuff[i][5]} Coolness**\n\n"
                in_top = True
            else:
                i+=1

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
                        total_achievements = num[0] # Self explanatory.
        if final_list != "":
            profile = discord.Embed(title=f"{target.display_name}'s Achievements", colour=discord.Colour.from_rgb(255,69,0), description=final_list)
            profile.set_thumbnail(url=target.avatar_url)
            profile.add_field(name="Total", value=f"{user_ach} of {total_achievements} Unlocked ({int((user_ach/total_achievements)*100)}%)", inline=False)
            await ctx.send(embed=profile)
                    



# A setup function the every cog has
def setup(bot):
    bot.add_cog(profile(bot))
