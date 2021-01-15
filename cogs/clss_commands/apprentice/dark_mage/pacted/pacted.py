import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
from sqlite3 import OperationalError
from asyncio.exceptions import TimeoutError

"""
INFO:
Uses ;blast, which is actually under Tamer.py
The rest of the commands, ;invoke and ;demon are here.
"""

class pacted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users_demons = {}
        self.demons_small = {
            "sugollix" : "https://i.pinimg.com/originals/f7/bf/8e/f7bf8ebeb031a970efe05cccdbc739cb.jpg",
            "ilixnith" : "https://64.media.tumblr.com/0d1004e4d1b3aa6efbf4ad1945d6f8f8/tumblr_oemuvhdbwA1tcdaigo1_1280.jpg",
            "foop" : "https://i.pinimg.com/originals/96/82/c5/9682c58dc4263dcfc9229c1c6747cc47.jpg",
            "trokgroor" : "https://gbf.wiki/images/thumb/f/f1/Summon_b_2030018000.png/408px-Summon_b_2030018000.png",
            "zollok" : "https://cdn.dribbble.com/users/537078/screenshots/11366007/media/352aea10a6fcb860a5e6f3bbd5b6e715.gif",
            "malakar" : "https://i.pinimg.com/736x/b7/8f/5b/b78f5b8cbdf2ec339a035c67b1a15dbe.jpg",
            "minehart" : "https://i.pinimg.com/originals/63/2b/07/632b079977fd041db073d7c82ec2691c.jpg"
        }
        self.hooks = [
            "usr1 heals usr2's bdypart injury",
            "usr1 rushes over to usr2 and has Sugollix use her healing waters on them",
            "usr1 pulls out an arrow from usr2's bdypart, then Sugollix heals the wound",
            "usr1 has Sugollix heal usr2",
            "usr1 and Sugollix heal usr2's broken bdypart",
            "usr1 surrounds usr2 in Sugollix's healing water, bringing them back to full health",
            "usr1 drags usr2 to safety and Sugollix heals them back up",
            "usr1 reattaches usr2's bdypart properly, with some help from Sugollix"
        ]

        self.minehart = {}

    @commands.command()
    @commands.guild_only()
    async def gloat(self, ctx): # Use `;gloat` for 5 AP to gain {1*(level)} stacks of **Confidence**, increasing your critical chance.
        if self.bot.users_classes[str(ctx.author.id)] == "pacted":
            uid = ctx.author.id

            demon = await h.get_demon(uid, self.bot)
            
            if demon:
                if demon == "malakar":
                    async with aiosqlite.connect('main.db') as conn:
                        async with conn.execute(f"select * from users where id = '{uid}';") as info:
                            user = await info.fetchone()
                    level = user[8] - 19
                    ap_works = await h.alter_ap(ctx.message, 5, self.bot)
                    if ap_works:
                        await h.add_effect(ctx.author, self.bot, "confidence", amount = 1*(level))
                        await ctx.send(f"Malakar's pride aura begins to affect you! You feel... well, prideful! (+{1*(level)} Confidence!)")
    
    @commands.command()
    @commands.guild_only()
    async def invoke(self, ctx): # Use `;gloat` for 5 AP to gain {1*(level)} stacks of **Confidence**, increasing your critical chance.
        if self.bot.users_classes[str(ctx.author.id)] == "pacted":
            uid = ctx.author.id

            demon = await h.get_demon(uid, self.bot)
            
            if demon:
                if demon == "minehart":
                    if demon == "minehart" and ctx.author.id not in self.minehart:
                        self.minehart[ctx.author.id] = 0
                    elif demon == "minehart" and ctx.author.id in self.minehart: 
                        amount = self.minehart[ctx.author.id]
                        if amount == 0:
                            await ctx.send("Minehart has no coolness stored!")
                        else:
                            await h.add_coolness(ctx.author.id, amount)
                            await ctx.send(f"Minehart's cloak shudders with envy... you gain {amount} coolness!")
                            self.minehart[ctx.author.id] = 0
                        



    @commands.command()
    @commands.guild_only()
    async def restore(self, ctx, target: discord.Member = None):
        if self.bot.users_classes[str(ctx.author.id)] == "pacted" and target and target != ctx.author:
            uid = ctx.author.id

            demon = await h.get_demon(uid, self.bot)
            
            if demon:
                if demon == "sugollix":
                    async with aiosqlite.connect('main.db') as conn:
                        async with conn.execute(f"select * from users where id = '{uid}';") as info:
                            user = await info.fetchone()
                    level = user[8] - 19
                    ap_works = await h.alter_ap(ctx.message, 2, self.bot)
                    if ap_works:
                        hook = random.choice(self.hooks)
                        body_part = random.choice(h.body_parts)
                        hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                        hook = hook.replace("bdypart", body_part)
                        hook = hook.replace("usr2", f"**{target.display_name}**")

                        if ctx.author.id in self.bot.server_boosters: # Check their maximum AP
                            max_ap = 40
                        else:
                            max_ap = 20

                        if str(ctx.author.id) in self.bot.users_ap:
                            ap_healed = random.randint(1,level*2)
                            try:
                                new_ap = self.bot.users_ap[str(target.id)] + ap_healed
                                if new_ap > max_ap:
                                    new_ap = max_ap
                                self.bot.users_ap[str(target.id)] = new_ap
                            except KeyError:
                                pass # User doesn't exist.
                        
                        await h.add_coolness(ctx.author.id, 5*ap_healed)

                        await ctx.send(f"{hook}, restoring {ap_healed} AP to them and personally gaining {ap_healed*5} coolness!")
    @commands.command()
    @commands.guild_only()
    async def demon(self, ctx): # Shoots an arrow at someone.
        if self.bot.users_classes[str(ctx.author.id)] == "pacted":
            uid = ctx.author.id

            if uid in self.users_demons:
                demon = self.users_demons[uid]
            else:
                async with aiosqlite.connect('classTables.db') as conn:
                    async with conn.execute(f"select uid, demon from pacted_demons where uid = '{uid}'") as u_info:
                        user_info = await u_info.fetchone()
                if user_info:
                    self.users_demons[uid] = user_info[1]
                    demon = user_info[1]
                    if demon == "minehart" and ctx.author.id not in self.minehart:
                        self.minehart[ctx.author.id] = 0
                elif user_info == None:
                    profile = discord.Embed(title=f"Annaisha's Totally Legal Demons!", colour=discord.Colour.from_rgb(255, 30, 30))
                    profile.add_field(name="Sugollix", value="A lustful demon capable of producing a healing liquid! Lets you heal people like a healer would!", inline=False)
                    profile.add_field(name="Ilixnith", value="A wrathful demon capable of fighting for long periods of time! Your criticals give you more coolness!", inline=False)
                    profile.add_field(name="Foop", value="A gluttonous and disgusting demon made of flesh! Your hot dogs are buffed!", inline=False)
                    profile.add_field(name="Trokgroor", value="A greedy demon, raised from a fallen king! You gain more daily gold!", inline=False)
                    profile.add_field(name="Zollok", value="A slothful demon, who always seems to be asleep! The longer you don't get a crit, the more your next crit does!", inline=False)
                    profile.add_field(name="Malakar", value="A prideful demon, they never shut up! Allows you to use `;gloat` for 5 AP, which gives you confidence, increasing your critical chance!", inline=False)
                    profile.add_field(name="Minehart", value="A envious demon, always looking around for others! Whenever someone gets a critical on you, Minehart saves a % of the coolness for you to gain with `;invoke`!", inline=False)
                    await ctx.send("You have no demon yet! Let me grab you some...! Here we are, I have the following fledgling demons!", embed=profile)
                    await ctx.send("Which demon would you like? **Choose carefully! This cannot be changed until you prestige!**")

                    def check(m: discord.Message):
                        return m.content and m.channel == ctx.message.channel and m.author == ctx.message.author

                    try:
                        chosen = await self.bot.wait_for('message', check=check, timeout=30)

                        if chosen.content.lower() in self.demons_small:
                            async with aiosqlite.connect('classTables.db') as conn:
                                async with aiosqlite.connect('classTables.db') as conn:
                                    await conn.execute(f"insert into pacted_demons values('{uid}', '{chosen.content.lower()}')")
                                    await conn.commit()
                            await ctx.send(f"Alright! Here you go! Hopefully you and {chosen.content.title()} become good friends!")
                            self.users_demons[uid] = chosen.content.lower()
                            if chosen.content.lower() == "minehart":
                                self.minehart[ctx.author.id] = 0
                            demon = None

                        else:
                            await ctx.send("That's not a valid demon name! Please try again!")        
                    except TimeoutError:
                        await ctx.send(f"{ctx.author.mention}, you took too long to choose! Please run the command again when you're ready.")

            if demon == "sugollix":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Lust", colour=discord.Colour.from_rgb(255,192,203)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A lustful demon capable of producing a healing liquid! Lets you heal people like a healer would!", inline=False)
                embed.add_field(name="Demon Power", value=f"Use `;restore` on a target, spending 2 AP, to restore 1 to {level*2} AP! This power increases with your demon's level!", inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)

            elif demon == "ilixnith":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Wrath", colour=discord.Colour.from_rgb(255,0,0)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A wrathful demon capable of fighting for long periods of time! Your criticals give you more coolness!", inline=False)
                embed.add_field(name="Demon Power", value=f"Your criticals give you {50*(1+level)} coolness! This number increases as your demon levels up!", inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)

            elif demon == "foop":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Gluttony", colour=discord.Colour.from_rgb(255,255,0)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A gluttonous and disgusting demon made of flesh! Your hot dogs are buffed!", inline=False)
                embed.add_field(name="Demon Power", value=f"Hot dogs give you {4+(level)} AP and {10+(5*level)} coolness! This increases as your demon levels up!", inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)

            elif demon == "trokgroor":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Greed", colour=discord.Colour.from_rgb(135,206,250)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A greedy demon, raised from a fallen king! You gain more daily gold!", inline=False)
                embed.add_field(name="Demon Power", value=f"Your daily gold reward has been raised to {100+(level*50)}! This increases as your demon levels up!", inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)

            elif demon == "zollok":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Sloth", colour=discord.Colour.from_rgb(255, 165, 0)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A slothful demon, who always seems to be asleep! The longer you attack and don't get a crit, the more your next crit does!", inline=False)
                embed.add_field(name="Demon Power", value=f"Your next crit gives you +{5*level} extra coolness per non-crit attack before it. This number resets when you get a crit, and this bonus increases as your demon levels up!", inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)

            elif demon == "malakar":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Pride", colour=discord.Colour.from_rgb(65,105,225)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A prideful demon, they never shut up! Allows you to `;gloat`, which gives you confidence, increasing your critical chance!", inline=False)
                embed.add_field(name="Demon Power", value=f"Use `;gloat` for 5 AP to gain {1*(level)} stacks of **Confidence**, increasing your critical chance.", inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)
            
            elif demon == "minehart":
                async with aiosqlite.connect('main.db') as conn:
                    async with conn.execute(f"select * from users where id = '{uid}';") as info:
                        user = await info.fetchone()
                level = user[8] - 19
                embed = discord.Embed(title=f"{demon.title()}, Minor Demon of Envy", colour=discord.Colour.from_rgb(191, 255, 0)) # {demon.title()}, Avatar of Lust
                embed.set_author(name=f"{ctx.author.display_name}'s Demon")
                embed.add_field(name="Level", value=level, inline=False)
                embed.add_field(name="Bio", value="A envious demon, always looking around for others! Whenever someone gets a critical on you, Minehart saves a % of the coolness for you to gain with `;invoke`!", inline=False)
                embed.add_field(name="Demon Power", value=f"When someone gets a critical on you, Minehart saves {2*level} coolness for you! Use `;invoke` to instantly gain the coolness!", inline=False)
                embed.add_field(name="Current Stored Coolness", value=self.minehart[ctx.author.id], inline=False)
                embed.set_image(url=self.demons_small[demon])

                await ctx.send(embed=embed)
            

# A setup function the every cog has
def setup(bot):
    bot.add_cog(pacted(bot))
