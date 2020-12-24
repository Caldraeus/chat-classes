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

        self.hooks_sand = [
            "usr1 covers usr2 in sand, suffocating them.",
            "usr1 creates quicksand, sucking usr2 into the ground!",
            "usr1 grabs usr2 by the throat, and slowly turns usr2 into sand. Wait, usr1, you can do that?!",
            "usr1 shoots a blast of sand through usr2's bdypart, obliterating it completely.",
            "usr1 creates a comically large spoon of sand, then beats usr2 to death with it.",
            "usr1 surrounds usr2 in sand, causing them to trip and fall off a cliff. Lmao, nice one usr2.",
            "usr1 bores a hole through usr2's bdypart using a small, but powerful, stream of sand.",
            "usr1 throws pocket sand into the eyes of usr2, then kicks them into a wall of spikes constructed of sand.",
            "usr1 throws a spiked ball of sand through usr2's torso, then slams usr2 into the ground.",
            "usr1 shoots sand into usr2's bdypart, then causes it to burst!"
        ]
        
        self.hooks_sand_mega = [
            "usr1 creates an entire sandstorm around usr2, completely enveloping them and leaving nothing but bones behind.",
            "usr1 opens up a hole in the sand below usr2, sending them falling thousands of feet down into the Earths core, until they impale on a large spike.",
            "usr1 grabs usr2 and lifts them into the air, slowly turning them into sand. usr2's scream slowly fade away, as their bones turn to sand, followed by the rest of their body.",
            "usr1 creates a large hammer of sand, then slams it into usr2. Then, usr1 causes usr2 to sink into the sand, burying them alive.",
            "usr1 slams usr2 into the ground, slowly forcing them deeper into the ground. usr2's screams are muffled by the sand as they finally perish.",
            "usr1 throws sand into usr2's eyes, then forces it to bore deeper into their brain.",
            "usr1 trips usr2, creating a bunch of spikes at the impact site. Needless to say, usr2's got a lot more holes in them now."
        ]

        self.hooks_lava = [
            "usr2 fires a lance of molten rock straight through usr2's bdyart."
        ]

        self.lava_mega_hooks = [

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
                    elif crit_check == 20:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness & + 1 Stone Shard | " + hook
                        self.shards[ctx.author.id] += 1
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🪨[MEGA-CRIT!]🪨** + 1000 Coolness | " + hook
                        self.shards[ctx.author.id] = 0
                        await h.add_coolness(ctx.author.id, 1000)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "dune wizard":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.shards:
                        self.shards[ctx.author.id] = 0

                    crit_check = random.randint(1,20)

                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_sand)

                    shards = self.shards
                    if shards[ctx.author.id] >= 0 and shards[ctx.author.id] < 100:
                        hook += f"\n\n*usr1 has {shards[ctx.author.id]}/100 sand!*"
                    elif shards[ctx.author.id] >= 100:
                        hook = random.choice(self.hooks_sand_mega)
                        crit_check = 100

                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check < 20:
                        self.shards[ctx.author.id] += random.randint(1,5)
                        await ctx.send(hook)
                    elif crit_check == 20:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness, + 50 Sand | " + hook
                        self.shards[ctx.author.id] += 50
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**🪨[MEGA-CRIT!]🪨** + 1000 Coolness | " + hook
                        self.shards[ctx.author.id] = 0
                        await h.add_coolness(ctx.author.id, 1000)
                        await ctx.send(hook)
        elif self.bot.users_classes[str(ctx.author.id)] == "igneous mage":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.shards:
                        self.shards[ctx.author.id] = 0

                    crit_check = random.randint(1,20)

                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_lava)

                    shards = self.shards
                    if shards[ctx.author.id] > 0 and shards[ctx.author.id] < 5:
                        hook += f"\n\n*usr1 has {shards[ctx.author.id]}/5 lava shards!*"
                    elif shards[ctx.author.id] >= 5:
                        hook = random.choice(self.lava_mega_hooks)
                        crit_check = 100

                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")

                    if crit_check < 20:
                        await ctx.send(hook)
                    elif crit_check == 20:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness & + 1 Lava Shard | " + hook
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
