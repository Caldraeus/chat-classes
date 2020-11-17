import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class entertainer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 whips out the bongos and plays some sweet sweet music.",
            "usr1 whips out a harp and plays some harmonious music for our ears. It's eye opening.",
            "usr1 does a nasty harmonica solo! Cool!",
            "usr1 does a cool drum solo that lasts 2 hours!",
            "usr1 does a cool steelpan perfromance! Groovy!",
            "usr1 plays the triangle. It is a truly beautiful performance.",
            "usr1 plays a cool song on the piano!",
            "usr1 shreds the guitar! Rock on!",
            "usr1 plays a nice song on the guitar. It's charming, really.",
            "usr1 sings a beautiful song about birds or something.",
            "usr1 pulls out a vibraphone from their pocket and starts playing an epic song!",
            "usr1 goes to town playing the washboard.",
            "usr1 is walking around with their street bagpipes playing some amazing music!",
            "usr1 plays the trumpet and leads a parade!",
            "usr1 does an amazing violin solo.",
            "usr1 plays the cello with expert speed and precision.",
            "usr1 beatboxes on the street!"
        ]
        self.hooks_win = [
            "usr1 does some crazy magic trick that even I don't understand! It's amazing!",
            "usr1 sings while playing the cabasa! It's really good!",
            "usr1 shreds some lines on their cast iron kazoo. It's amazing!",
            "usr1 pops off while playing the cowbell, creating music so epic it rips a hole in spacetime!",
            "usr1 whips out a pair of spoons and goes to town, playing music so epic it causes all violence in a 50 KM area to instantly stop!",
            "usr1 slowly pulls out a jar of mayo. Then, usr1 manipulates it in such a way that it plays music so pure, so beautiful, that everyone around usr1 begins to cry."
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def perform(self, ctx): 
        if self.bot.users_classes[str(ctx.author.id)] == "entertainer":
            ap_works = await h.alter_ap(ctx.message, 5, self.bot)
            if ap_works:
                crit_check = random.randint(1,20)
                body_part = random.choice(h.body_parts)

                goal = random.randint(1,3) # 1 = XP | 2 = GOLD | 3 = COOLNESS

                if crit_check < 20:
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")

                    if goal == 1:
                        async with aiosqlite.connect('main.db') as conn:
                            xp_gained = random.randint(25,75)
                            hook+=f"\n\n*Someone tipped {xp_gained} XP!*"
                            async with conn.execute(f"select exp from users where id = '{ctx.author.id}'") as exp:
                                old_exp = await exp.fetchone()
                                new_exp = old_exp[0] + xp_gained
                                await conn.execute(f"update users set exp = {new_exp} where id = '{ctx.author.id}';")
                                await conn.commit() 

                    elif goal == 2:
                        gold_gained = random.randint(10,100)
                        hook+=f"\n\n*Someone tipped {gold_gained} gold!*"
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select gold from users where id = '{ctx.author.id}'") as money:
                                old_gold = await money.fetchone()
                                new_gold = old_gold[0] + gold_gained
                                await conn.execute(f"update users set gold = {new_gold} where id = '{ctx.author.id}';")
                                await conn.commit() 
                    else:
                        coolness_added = random.randint(50,200)
                        hook+=f"\n\n*Someone tipped {coolness_added} coolness!*"
                        await h.add_coolness(ctx.author.id, coolness_added)

                    await ctx.send(f"**🎵[SUCCESS]🎵** | {hook}")

                elif crit_check < 20:
                    hook = random.choice(self.hooks_win)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")

                    if goal == 1:
                        async with aiosqlite.connect('main.db') as conn:
                            xp_gained = random.randint(75,100)
                            hook+=f"\n\n*Someone tipped {xp_gained} XP!*"
                            async with conn.execute(f"select exp from users where id = '{ctx.author.id}'") as exp:
                                old_exp = await exp.fetchone()
                                new_exp = old_exp[0] + xp_gained
                                await conn.execute(f"update users set exp = {new_exp} where id = '{ctx.author.id}';")
                                await conn.commit() 

                    elif goal == 2:
                        gold_gained = random.randint(100,150)
                        hook+=f"\n\n*Someone tipped {gold_gained} gold!*"
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select gold from users where id = '{ctx.author.id}'") as money:
                                old_gold = await money.fetchone()
                                new_gold = old_gold[0] + gold_gained
                                await conn.execute(f"update users set gold = {new_gold} where id = '{ctx.author.id}';")
                                await conn.commit() 
                    else:
                        coolness_added = random.randint(100,200)
                        hook+=f"\n\n*Someone tipped {coolness_added} coolness!*"
                        await h.add_coolness(ctx.author.id, coolness_added)

                    await ctx.send(f"**🎵[CRITICAL SUCCESS]🎵** | {hook}")
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(entertainer(bot))
