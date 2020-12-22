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

class class_comands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    async def start(self, ctx):
        random.seed(ctx.author.id)
        num = random.randint(1,4)
        clss = h.base_classes[num]
        lead = "a"
        if num == 4:
            lead += "n"
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select id from users where id = '{ctx.message.author.id}';") as person:
                user = await person.fetchone()
                if user:
                    await ctx.send("You already have a profile! Use `;class` to see what you can do!")
                else:
                    print(f"User {ctx.message.author.id} doesn't exist")
                    ### Add user to database
                    await conn.execute(f"insert into users values('{ctx.message.author.id}', '{clss.lower()}', 0, 0, 'No skills', 0, '0', '', 1, 0, False, 0, 8)")
                    async with conn.execute(f"select id, class, achievements, ap from users;") as people:
                        usrs = await people.fetchall()
                        for guy in usrs:
                            user_ach = guy[2].split("|")
                            unlocked = []
                            for stringnum in user_ach: # Just for the if statement. I really hate this and want to fix it eventually.
                                unlocked.append(int(stringnum))
                                
                            self.bot.registered_users[str(guy[0])] = unlocked
                    await conn.commit()
                    ###
                    await ctx.send(f"{ctx.author.mention}, you are {lead} {clss.lower()}. Use `;profile` to view your profile! Use `;classinfo` to see your class-specific commands!")
                    self.bot.users_classes[str(guy[0])] = clss.lower()
                    self.bot.users_ap[str(guy[0])] = 8
        
    @commands.command(aliases=["class"])
    @commands.guild_only()
    async def classinfo(self, ctx, *, clss = None):
        if not clss:
            clss = self.bot.users_classes[str(ctx.author.id)]
        clss = clss.lower()
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select * from classes where class_name = '{clss}';") as cinfo:
                class_info = await cinfo.fetchall()
                class_info = class_info[0]
                profile = discord.Embed(title=f"{clss.title()}'s Info", colour=discord.Colour.from_rgb(128, 128, 128), description=class_info[1])
                profile.add_field(name="Previous Class", value=class_info[3], inline=False)
                abilities = class_info[5].split("|")
                final = ""
                for abil in abilities:
                    final+=abil+"\n"
                profile.add_field(name="Class Abilities", value=final, inline=False)
        
        await ctx.send(embed=profile)
    
    @commands.command()
    @commands.guild_only()
    async def test(self, ctx):
        async with aiohttp.ClientSession() as session:
            # testhook = await ctx.channel.create_webhook(name="Test")
            url = await h.webhook_safe_check(ctx.channel)
            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await hook.send(content=ctx.message.content, username=ctx.message.author.display_name, avatar_url=ctx.message.author.avatar_url)
    
    @commands.command(aliases=["prog"])
    @commands.guild_only()
    async def progression(self, ctx, *, clss = None):
        if clss:
            classes = []
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select * from classes where preclass = '{clss}';") as cinfo:
                    class_info = await cinfo.fetchall()

            profile = discord.Embed(title=f"🌟 {clss.title()} Class Progression 🌟", colour=discord.Colour.from_rgb(255, 165, 0))
            profile.set_footer(text=f"A lock symbol next to a class name means there's an achievement required to choose it!", icon_url="")
            for potential_class in class_info:
                classes.append(potential_class)
                if potential_class[4] != 0: # It's an achievement locked class...
                    profile.add_field(name=f"🔒 | {potential_class[0].title()}", value=potential_class[1], inline=False)
                elif potential_class[4] == 0:
                    profile.add_field(name=potential_class[0].title(), value=potential_class[1], inline=False)

            if classes != []:
                await ctx.send(embed=profile)
            else:
                await ctx.send("That class either doesn't exist or doesn't have any class progressions!")


    @commands.command()
    @commands.guild_only()
    async def classup(self, ctx):
        uid = ctx.author.id
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select * from users where id = '{uid}';") as info:
                user = await info.fetchone()
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select exp, level from users where id = '{ctx.author.id}';") as profile:
                prof = await profile.fetchone()

        xp = prof[0]

        current_lvl = prof[1]
        if (user[8]+1) % 10 == 0 and (xp >= h.max_xp(current_lvl) and ((prof[1]+1) % 10 == 0)): # I think this makes sure they are high enough level 
            ###
            user_ach = user[6].split("|")
            clss = user[1].replace("_"," ")
            clss = clss.lower()
            allowed_classes = []

            if clss.title() in h.base_classes.values():
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from classes where preclass = '{clss}' or preclass = 'origin';") as cinfo:
                        class_info = await cinfo.fetchall()
            else:
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from classes where preclass = '{clss}';") as cinfo:
                        class_info = await cinfo.fetchall()

            profile = discord.Embed(title=f"🌟 CLASS-UP! 🌟", colour=discord.Colour.from_rgb(255, 165, 0))
            for potential_class in class_info:
                if potential_class[4] != 0 and str(potential_class[4]) in user_ach: # It's an achievement locked class...
                    profile.add_field(name=potential_class[0].title(), value=potential_class[1], inline=False)
                    allowed_classes.append(potential_class[0].lower())
                elif potential_class[4] == 0:
                    profile.add_field(name=potential_class[0].title(), value=potential_class[1], inline=False)
                    allowed_classes.append(potential_class[0].lower())

            await ctx.send(embed=profile)
            await ctx.send(f"{ctx.author.mention} which class do you wish to become? Say `none` to cancel.")
            
            def check(m: discord.Message):
                return m.content and m.channel == ctx.message.channel and m.author == ctx.message.author

            try:
                chosen = await self.bot.wait_for('message', check=check, timeout=30)
            except:
                await ctx.send(f"{ctx.author.mention}, you took too long to choose! Please run the command again when you're ready.")

            if chosen.content.lower() in allowed_classes:
                if ctx.author.id in self.bot.notified:
                    self.bot.notified.remove(ctx.author.id)
                await ctx.send(f"Alright! Here we go! \n\n*3...*\n\n*<:STEASnothing:517873442381627392>2...*\n\n*<:STEASnothing:517873442381627392><:STEASnothing:517873442381627392>1... and...!*\n\n<:STEASnothing:517873442381627392><:STEASnothing:517873442381627392><:STEASnothing:517873442381627392><:STEASnothing:517873442381627392>☁️ **P O O F !** ☁️\n\n{ctx.author.mention} is now a **{chosen.content.title()}**! Congratulations!")
                # Time to edit.
                async with aiosqlite.connect('main.db') as conn:
                    await conn.execute(f"update users set class = '{chosen.content.lower()}', exp = 0, level = {user[8]+1} where id = '{ctx.author.id}'")
                    await conn.commit()

                self.bot.users_classes[str(ctx.author.id)] = chosen.content.lower()
                self.bot.user_status[int(ctx.author.id)] = []
            else:
                await ctx.send("Class-up cancelled! If you didn't mean for this to happen, make sure you spelt the class name correctly!")
        else:
            await ctx.send("Sorry, you can't change classes yet! Come back when you're higher level.")



# A setup function the every cog has
def setup(bot):
    bot.add_cog(class_comands(bot))
