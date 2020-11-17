import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class rogue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 stabs usr2 in the bdypart.",
            "usr1 sneaks up on usr2, stabbing them in the bdypart.",
            f"usr1 walks up to usr2, then stabs them a total of {random.randint(2,20)} times in the bdypart. Yeah, I think that'll do it.",
            "usr1 throws one knife into usr2's bdypart, then runs up and slits their throat. Brutal, man! Brutal!",
            "usr1 sneaks up behind usr2 and stabs them, ending them quickly.",
            "usr1 stabs usr2 28 times. 28 stab wounds!",
            "usr1 surgically removes usr2's bdypart. Well, maybe not *surgically*, but you get the idea.",
            "usr1 slowly pushes their knife into usr2's bdypart. usr1 smiles evilly.",
            "usr1 is in need of bdypart. usr2 happens to have bdypart. You know where this goes.",
            f"usr1 stands across from usr2. A standoff. usr1 smiles, revealing the contents of their trenchcoat. It's... knives. To be exact, it's {random.randint(10,200)} knives. usr1 throws each and every knife at usr2. Lets just say, usr2 didn't make it out.",
            "usr1 is out at a romantic dinner with usr2. usr1 waits until no one is looking, then grabs the butterknife, cutting out usr2's bdypart, and making a dash for it.",
            "usr1 cuts off usr2's bdypart.",
            "usr1 stabs usr2.",
            "usr1 leaps onto usr2's back, then plunges their knives into usr2's chest. FATALITY!",
            "usr1 feels a sudden onset of bloodlust. Unfortunately, usr2 is the closest person. usr1 is now the proud owner of usr2's bdypart.",
            "usr1 stands across from usr2.\n\n'Do you really think you can stop me?' laughs usr1.\n\n'Ha! You overestimate your own power' says usr2.\n\nusr2 attacks usr1, but in the blink of an eye, usr1 is behind usr2. \n\n'I'm going to cut out your bdypart, stuff it, and put it on my mantle.'\n\nusr2 is struck with fear as usr1 stabs them. usr1 smiles evilly. The deed is done."
        ]

        self.hooks_c = [
            "usr1 cuts out usr2's bdypart while they're asleep, and sells it on the black market for 50$.",
            "usr1 breaks into usr2's home and stabs them in the bdypart.",
            "usr1 sneaks into usr2's home, yoinks some valuables, then suffocates usr2 with a pillow.",
            "usr1 stabs usr2 in an alleyway and steals their wallet. Yoink!",
            "usr1 stabs usr2 on their way back home, then steals their purse.",
            "usr1 shanks usr2 in the back and runs away.",
            "usr1 kicks usr2 in front of an oncomming train.",
            "usr1 stabs usr2 in the bdypart, then steals their kidneys.",
            "usr1 stabs usr2 with a pencil in a bar, then robs the bar and runs away.",
            "usr1 tricks usr2 into giving them their credit card information, then stabs them in the bdypart.",
            "usr1 chases usr2 down the street then chloroforms them before stabbing them.",
            "usr1 follows usr2 to their car and sneaks into the trunk. Once usr2 arrives home, usr1 jumps out and stabs them before stealing their car.",
            "usr1 pretends to be a homeless guy and scams usr2. Oh, then stabs them. Like 15 times. It was a bit unnecessary, really."
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def shank(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370 and await h.can_attack(ctx.author.id, target.id):
            if self.bot.users_classes[str(ctx.author.id)] == "rogue":
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
                        hook = "**✨[CRITICAL BACKSTAB]✨** + 200 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 200)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "criminal":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works:
                    crit_check = random.randint(1,20)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_c)
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
    bot.add_cog(rogue(bot))
