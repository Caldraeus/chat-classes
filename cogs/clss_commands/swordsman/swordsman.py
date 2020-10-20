import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class swordsman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 heaves their sword into usr2, completely removing their bdypart. Ouch!",
            "usr1 charges at usr2, impaling usr2 upon their sword.",
            "usr1 stands across from usr2.\n\n'So, it comes to this, does it?'\n\nusr1 smiles. 'I always knew it would.'\n\n'I guess we'll never be able to go on that fishing trip, huh?'\n\n'Yeah, I guess not.'\n\nusr1 raises their sword, and with one decisive strike, removes usr2's bdypart. They fall over, dead. usr1 wipes tears off of their face as they walk away.",
            "usr1 heaves their sword into usr2's bdypart. Damn!",
            "usr1 blocks usr2's first attack, then flips them over using their shield. usr1 then follows that up with a pluging attack into usr2's bdypart.",
            "usr1 shoulder bashes usr2 off a cliff.",
            "usr1 beats usr2 to death with their shield. That's gotta hurt.",
            "usr1 headbuts usr2, then swings their sword into usr2's bdypart. Ouch!",
            "usr1 kicks usr2 into a wall, then rams their sword into usr2's bdypart.",
            "usr1 parries usr2's first attack, then follows it up with a swift strike to usr2's bdypart.",
            "usr1 is in a bad mood. usr2 happens to be the closest person at the time, and sensing usr1's bloodlust, begins to run. It is futile. usr1 charges at usr2 and impales their bdypart. Someone woke up on the wrong side of the bed.",
            "usr1 throws pocket sand at usr2, then proceeds to cut off their bdypart.",
            "usr1 throws themself at usr2, chopping off their bdypart.",
            "usr1 cuts off usr2's bdypart, then beats them to death with it."
        ]
    pass

    @commands.command(aliases=['slice'])
    @commands.guild_only()
    async def slic(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "swordsman":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works:
                    crit_check = random.randint(1,20)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check != 20:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(swordsman(bot))
