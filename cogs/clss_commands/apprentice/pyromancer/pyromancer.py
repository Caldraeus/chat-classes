import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
"""
pyrolevels = {}
pyrolevels[69420] = 1

print(pyrolevels)
if 69420 in pyrolevels:
  pyrolevels[69420] += 1

print(pyrolevels)
"""
class pyromancer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 shoots a fireball at usr2.",
            "usr1 douses usr2 in gasoline, then tosses a fireball at them.",
            "usr2 shoots a bolt of fire straight into usr2's bdypart, incinerating it immediately.",
            "usr1 lights their hands on fire, then plunges them into usr2's bdypart, burning usr2's bdypart beyond recognition.",
            "usr1 creates a pillar of fire beneath usr2, immolating them.",
            "usr1 creates a wall of fire right in front of usr2, who doesn't notice until it's too late.",
            "usr1 shoots a blast of white hot fire at usr2.",
            "'usr2... I hope you're ready to feel the heat.'\n\n'Ha! How long did you practice that one, usr1? That was really dumb.'\n\nusr1 scoffs, then generates a huge ball of fire.\n\nusr2 realises their mistake.\n\nusr1 fires the large ball of fire directly at usr2, burning their bdypart incredibly badly and singing the rest of their body.",
            "usr1 sneaks up on usr2, then lights usr2's bdypart on fire! Owch!",
            "usr1 surrounds usr2 in a cage of fire, then leaves usr2 ther to burn. Slowly. Painfully.",
            "usr1 claps their hands together, sending a wave of flames at usr2. usr2 attempts to dodge, but isn't that good at it, and takes the full force of the flames, combusting!"
        ]

        self.mega_hooks = [
            "usr1's inner fire burns at maximum power, allowing them to shoot a massive fireball at usr2, completely deleting them from existence!",
            "usr1's inner fire begins exploding, eventually erupting into a massive nova, reducing usr2 to mere atoms!",
            "usr1 can barely contain their inner fire, and release a directional super-blast at usr2!",
            "usr1's inner fire reaches peak levels, before completely destroying any trace of usr2!",
            "usr1's inner fire causes them to burst into flames! They then go and hug usr2, completely reducing them to ash!",
            "usr1 releases all of their inner fire at usr2, completely burning away usr2 and anything within a 20 KM radius!",
            "usr2 sees the sun. Wait, no, that's not the sun, that's usr1! usr2 begins to run, but it's too late. usr1 collides with usr2, destroying them.",
            "usr1 can no longer control their inner fire, and release a burst of pure flame directly through the middle of usr2. Nothing remains of usr2 after.",
            "usr1 reaches their inner fire's limit, releasing a concentrated beam of fire straight through usr2's head, legs, arms and bdypart. usr2 collapses, dead."
        ]
        self.pyrolevels = {}
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def torch(self, ctx, target: discord.Member = None): 
        if target and target != ctx.author and target.id != 713506775424565370:
            if (self.bot.users_classes[str(ctx.author.id)] == "pyromancer" or self.bot.users_classes[str(ctx.author.id)] == "multi-mage"):
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] = 0
                    elif ctx.author.id in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] += random.randint(1,17)

                    crit_check = 0
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)

                    pyrolevels = self.pyrolevels
                    if pyrolevels[ctx.author.id] <= 25:
                        hook += f"\n\n*usr1's inner fire kindles lightly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 50:
                        hook += f"\n\n*usr1's inner fire burns at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 75:
                        hook += f"\n\n*usr1's inner fire burns strongly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 99:
                        hook += f"\n\n*usr1's inner fire roars at {pyrolevels[ctx.author.id]+20}°C...!*"
                    elif pyrolevels[ctx.author.id] >= 100:
                        hook = random.choice(self.mega_hooks)
                        crit_check = 100
                        pyrolevels[ctx.author.id] = -10
                    
                    if crit_check != 100:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                        
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🔥[OVERHEAT!]🔥** + 75 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 75)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "flameborn":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] = 0
                    elif ctx.author.id in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] += random.randint(10,20)

                    crit_check = 0
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)

                    pyrolevels = self.pyrolevels
                    if pyrolevels[ctx.author.id] <= 25:
                        hook += f"\n\n*usr1's inner fire kindles lightly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 50:
                        hook += f"\n\n*usr1's inner fire burns at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 75:
                        hook += f"\n\n*usr1's inner fire burns strongly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 99:
                        hook += f"\n\n*usr1's inner fire roars at {pyrolevels[ctx.author.id]+20}°C...!*"
                    elif pyrolevels[ctx.author.id] >= 100:
                        hook = random.choice(self.mega_hooks)
                        crit_check = 100
                        pyrolevels[ctx.author.id] = -10

                    if crit_check != 100:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                        
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🔥[OVERHEAT!]🔥** + 75 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 75)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "flame tongue":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] = 0
                    elif ctx.author.id in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] += random.randint(10,20)

                    crit_check = 0
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)

                    pyrolevels = self.pyrolevels
                    if pyrolevels[ctx.author.id] <= 50:
                        hook += f"\n\n*usr1's inner fire kindles lightly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 75:
                        hook += f"\n\n*usr1's inner fire burns at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 100:
                        hook += f"\n\n*usr1's inner fire burns strongly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 150:
                        hook += f"\n\n*usr1's inner fire roars at {pyrolevels[ctx.author.id]+20}°C...!*"
                    elif pyrolevels[ctx.author.id] >= 200:
                        hook = random.choice(self.mega_hooks)
                        crit_check = 100
                        pyrolevels[ctx.author.id] = -10

                    if crit_check != 100:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                        
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🔥[EXTREME OVERHEAT!]🔥** + 250 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 75)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "fire lord":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] = 0
                    elif ctx.author.id in self.pyrolevels:
                        self.pyrolevels[ctx.author.id] += random.randint(1,17)

                    crit_check = 0
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)

                    pyrolevels = self.pyrolevels
                    if pyrolevels[ctx.author.id] <= 25:
                        hook += f"\n\n*usr1's inner fire kindles lightly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 50:
                        hook += f"\n\n*usr1's inner fire burns at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 75:
                        hook += f"\n\n*usr1's inner fire burns strongly at {pyrolevels[ctx.author.id]+20}°C...*"
                    elif pyrolevels[ctx.author.id] <= 99:
                        hook += f"\n\n*usr1's inner fire roars at {pyrolevels[ctx.author.id]+20}°C...!*"
                    elif pyrolevels[ctx.author.id] >= 100:
                        hook = random.choice(self.mega_hooks)
                        crit_check = 100
                        pyrolevels[ctx.author.id] = -10

                    if crit_check != 100:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                        
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🔥[ROYAL OVERHEAT!]🔥** + 75 Coolness, + 200 Gold | " + hook
                        await h.add_coolness(ctx.author.id, 75)
                        await h.add_gold(ctx.author.id, 200, self.bot)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(pyromancer(bot))
