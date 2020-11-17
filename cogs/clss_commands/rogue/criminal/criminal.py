import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class criminal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 robs a frail old lady.",
            "usr1 robs a bar using a really scary looking prop sword.",
            "usr1 mugs a normal citizen walking down the sidewalk.",
            "usr1 commits tag evasion.",
            "usr1 murders their neighbor, then takes their house.",
            "usr1 beats the crap out of some kid and takes their lunch money.",
            "usr1 breaks into an abandoned Chuck E. Cheese and spraypaints a wall. Dangerous!",
            "usr1 commits a crime in the nth dimension, and avoids the time police.",
            "usr1 violates the laws of physics and gets away with it. How evil!",
            "usr1 pickpockets one of their friends.",
            "usr1 catfishes a celebrity, then robs them.",
            "usr1 robs a bank using a prop lightsaber."
        ]
        self.hooks_fail = [
            "usr1 attempts to rob some dude named Steve, but quickly learns that Steve is a blackbelt. Ouch.",
            "usr1 tries to rob me, of all people. I smite them, and they learn their place.",
            "usr1 tries to rob Shia LaBeouf, forgetting that he is actually a dangerous cannibal. It does not go well for usr1, and they come out of the encounter missing a bdypart.",
            "usr1 tries to rob god. It does not work, and usr1 is now missing a bdypart.",
            "usr1 tries to rob a wizard, but gets struck in the face by several fireballs.",
            "usr1 tried to rob a library, but the librarian was half ninja and beats the crap out of usr1.",
            "usr1 tries to rob a dog, but then feels really bad about it and changes their mind."
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def crime(self, ctx): 
        if self.bot.users_classes[str(ctx.author.id)] == "criminal":
            ap_works = await h.alter_ap(ctx.message, 5, self.bot)
            if ap_works:
                crit_check = random.randint(1,20)
                body_part = random.choice(h.body_parts)

                goal = random.randint(1,3) # 1 = XP | 2 = GOLD | 3 = COOLNESS

                if crit_check < 15:
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")

                    if goal == 1:
                        async with aiosqlite.connect('main.db') as conn:
                            xp_gained = random.randint(25,75)
                            hook+=f"\n\n*Stole {xp_gained} XP!*"
                            async with conn.execute(f"select exp from users where id = '{ctx.author.id}'") as exp:
                                old_exp = await exp.fetchone()
                                new_exp = old_exp[0] + xp_gained
                                await conn.execute(f"update users set exp = {new_exp} where id = '{ctx.author.id}';")
                                await conn.commit() 

                    elif goal == 2:
                        gold_gained = random.randint(10,100)
                        hook+=f"\n\n*Stole {gold_gained} gold!*"
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select gold from users where id = '{ctx.author.id}'") as money:
                                old_gold = await money.fetchone()
                                new_gold = old_gold[0] + gold_gained
                                await conn.execute(f"update users set gold = {new_gold} where id = '{ctx.author.id}';")
                                await conn.commit() 
                    else:
                        coolness_added = random.randint(50,200)
                        hook+=f"\n\n*Gained {coolness_added} coolness!*"
                        await h.add_coolness(ctx.author.id, coolness_added)

                    await ctx.send(f"**💰[SUCCESS]💰** | {hook}")

                elif crit_check >= 15:
                    jail_check = random.randint(1,20)
                    if jail_check == 1:
                        await ctx.send("**🚔[TOTAL FAILURE]🚔** | You fail so badly at committing a crime, that you get caught red handed and thrown into jail. You lose **all** of your AP!")
                        self.bot.users_ap[str(ctx.author.id)] = 0
                    else: 
                        hook = random.choice(self.hooks_fail)
                        hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                        hook = hook.replace("bdypart", random.choice(h.body_parts))

                        hook = "**🚔[FAILURE]🚔** | " + hook

                        if goal == 1:
                            async with aiosqlite.connect('main.db') as conn:
                                xp_gained = random.randint(25,75)*-1
                                hook+=f"\n\n*Lost {-1*xp_gained} XP!*"
                                async with conn.execute(f"select exp from users where id = '{ctx.author.id}'") as exp:
                                    old_exp = await exp.fetchone()
                                    new_exp = old_exp[0] + xp_gained
                                    if new_exp < 0:
                                        new_exp = 0
                                    await conn.execute(f"update users set exp = {new_exp} where id = '{ctx.author.id}';")
                                    await conn.commit() 
                        elif goal == 2:
                            gold_gained = random.randint(10,200)*-1
                            hook+=f"\n\n*Lost {-1*gold_gained} gold!*"
                            async with aiosqlite.connect('main.db') as conn:
                                async with conn.execute(f"select gold from users where id = '{ctx.author.id}'") as money:
                                    old_gold = await money.fetchone()
                                    new_gold = old_gold[0] + gold_gained
                                    if new_gold < 0:
                                        new_gold = 0
                                    await conn.execute(f"update users set gold = {new_gold} where id = '{ctx.author.id}';")
                                    await conn.commit() 
                        else:
                            coolness_added = random.randint(50,250)*-1
                            hook+=f"\n\n*Lost {-1*coolness_added} coolness!*"
                            await h.add_coolness(ctx.author.id, coolness_added)
                        
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(criminal(bot))
