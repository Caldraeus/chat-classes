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
            "usr1 cuts off usr2's bdypart, then beats them to death with it.",
            "usr1 throws their sword into usr2's bdypart, then pulls it out and chops their head off."
        ]

        self.hooks_w = [
            "usr1 slams their sword into usr2's bdypart, eviscerating it.",
            "usr1 chops usr2's bdypart off.",
            "usr1 throws their sword into usr2's chest, then dropkicks it deeper through them.",
            "usr1 slashes usr2's bdypart off, then stomps on it.",
            "usr1 throws a javelin through usr2's bdypart, then cuts them in half with their sword.",
            "usr1 charges at usr2, shoving their sword through usr2's bdypart and slamming them to the floor.",
            "usr1 shoots a crossbow bolt into usr2's bdypart, then runs up and cuts their leg off, causing usr2 to fall down and get further impaled by the crossbow bolt. A bit overkill, usr1. A bit overkill.",
            "usr1 stands on their knees in front of usr2.\n\n'So, any last words, usr1?'\n\n'Yeah. Just one...'\n\nusr1 then headbuts usr2, knocking them down, then steals usr2's weapon and beats them to death with it. usr1 is breathless, but alive.",
            "usr1 kicks usr2 in the stomach, sending them flying, before slashing them in the bdypart.",
            "usr1 throws a dagger into usr2's knee, crippling them. Then, usr1 runs up and impales usr2's bdypart on their sword.",
            "usr1 knees usr2 in the neck, then throws them across the room into a wall before jumping on them with their sword, killing them.",
            "usr2 is locked in battle with usr1. usr2 keeps throwing attack after attack at usr2, but usr1 avoids them all, then charges into usr2, stabbing them through the bdypart.",
            "usr1 grabs usr2's arm and twists it behind their back, then beats usr2 to death with a club.",
            f"usr1 kicks usr2 into a wall before slashing them in the back {random.randint(2,100)} times. Ouch!"
        ]

        self.hooks_s = [
            "usr1 parries usr2's first attack, then slams their katana into their side."
        ]
    pass

    @commands.command(aliases=['slice'])
    @commands.guild_only()
    async def slic(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370 and await h.can_attack(ctx.author.id, target.id):
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
            elif self.bot.users_classes[str(ctx.author.id)] == "warrior":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works:
                    crit_check = random.randint(1,20)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_w)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check != 20:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "samurai":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works:
                    crit_check = random.randint(1,20)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_s)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check != 20:
                        await ctx.send(hook)
                    else:
                        hook = "**🌸[SENBONZAKURA!]🌸** + 250 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 250)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(swordsman(bot))
