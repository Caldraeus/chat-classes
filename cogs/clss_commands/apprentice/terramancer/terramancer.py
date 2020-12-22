import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class terramancer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 levitates a boulder over usr2, then lets it drop. Ouch.",
            "usr1 summons two walls of stone, then squashes usr2. Gross!",
            "usr1 covers themself in stone, then runs straight through usr2!",
            "usr1 creates a spear of earth, and throws it through usr2's bdypart.",
            "usr1 raises a plethora of spikes below usr2, impaling them before they have time to react.",
            "usr1 opens a chasm below usr2. Bye bye!",
            "usr1 blocks usr2's attack with a stone shield, then bashes their head in with the stone shield.",
            "usr1 creates a stone hammer and cripples usr2, then proceeds to crush usr2's bdypart with the hammer.",
            "usr1 grabs usr2's head, then slams it into a hole in the ground, suffocating them.",
            "usr1 throws a bunch of rocks at usr2, *stoning* them to death. Get it?",
            "usr1 is at the top of the hill, and sees usr2 at the bottom. They create a giant boulder and roll it down at them, crushing them!",
            "usr1 summons a spike from behind usr2, impaling them. usr1 then summons four additional spikes from the ground, impaling usr2 four more times, then letting them drop.",
            "usr1 summons a sphere cage of stone around usr2, suffocating them. Slowly.",
            "usr1 creats a stone hammer and bashes in usr2's bdypart. Ouch.",
            "usr1 throws a stone hammer straight through usr2.",
            "usr1 lifts up the ground below usr2 to a great height, then flips it. usr2 falls, then smashes to the ground. Splat!",
            "usr1 launches 3 stone spheres at usr2, smashing in their head, legs and bdypart."
        ]

        self.mega_hooks = [
            "usr1 opens a hole to the earths core, and tosses usr2 into it. Sayonara!",
            "usr1 covers their fist in stone, then punches a hole straight through usr2! Brutal!",
            "usr1 unearths a skyscraper, then slams it into usr2. There is nothing left behind.",
            "usr1 collects enough stone to create a giant golem, which picks up usr2 and squashes them.",
            "usr1 quickly beheads usr2 with a disk of stone, then dices the rest of their body into nice, square bits.",
            "usr1 shoots a bunch of stone pellets through usr2, leaving them with a bunch of bloody holes.",
            "usr1 creates a giant stone hammer, then repeatedly smashes usr2's bdypart, killing them. Brutality!"
        ]

        self.shards = {}
    pass

    @commands.command()
    @commands.guild_only()
    async def stone(self, ctx, target: discord.Member = None): 
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "terramancer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.shards:
                        self.shards[ctx.author.id] = 0

                    crit_check = random.randint(1,20)

                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)

                    shards = self.shards
                    if shards[ctx.author.id] > 0 and shards[ctx.author.id] < 5:
                        hook += f"\n\n*usr1 has {shards[ctx.author.id]}/5 stone shards!*"
                    elif shards[ctx.author.id] >= 5:
                        hook = random.choice(self.mega_hooks)
                        crit_check = 100

                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check < 20:
                        await ctx.send(hook)
                    elif crit_check == 20 and ~(crit_check >= 20):
                        hook = "**✨[CRITICAL]✨** + 100 Coolness & + 1 Stone Shard | " + hook
                        self.shards[ctx.author.id] += 1
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🪨[MEGA-CRIT!]🪨** + 1000 Coolness | " + hook
                        self.shards[ctx.author.id] = 0
                        await h.add_coolness(ctx.author.id, 1000)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(terramancer(bot))
