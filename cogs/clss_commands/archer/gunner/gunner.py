import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class gunner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 shoots usr2.",
            "usr1 jumps over usr2, shooting them from above! Nice!",
            "usr1 quickly fires six shots into usr2, striking them in the arm, leg and bdypart.",
            "usr1 shoots usr2 in the back as they run away.",
            "usr1 shoots usr2 in the bdypart.",
            "usr1 tackles usr2, then throws them into the wall before slowly bringing their gun to usr2's head. Bam!",
            "usr1 throws their gun into usr2's head, knocking them out. Hey, if it works, it works!",
            "usr1 reloads their gun while running at usr2, then slides on their knees while firing multiple shots into usr2.",
            "usr1 ricochets 2 bullets off of the wall and strikes usr2.",
            "usr1 trips usr2, then fires their gun into usr2's bdypart. Ouch!",
            "usr1 writes usr2's name on a bullet. Years pass. Then, the moment comes - usr1 stands across from usr2, and before anyone can say a word, fires the bullet into usr2's head. It is done. usr1 lets out a sigh of relief.",
            "usr1 shoots usr2 in the legs, causing usr2 to fall over and off a bridge.",
            "usr1 kicks usr2 off a cliff, and as usr2 falls, shoots them 3 times.",
            "usr1 pulls out a second revolver and fires blindly at usr2. Needless to say, usr2 has a lot more holes than before.",
            "usr1 shoots usr2 in the bdypart. Which is really rude, actually. usr2 gives them a scowl and hobbles away.",
            "usr1 kicks usr2 into the wall before firing multiple shots into usr2."
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def shoot(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370 and await h.can_attack(ctx.author.id, target.id, ctx):
            if self.bot.users_classes[str(ctx.author.id)] == "gunner":
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
                        hook = "**✨[HEADSHOT]✨** + 150 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 150)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(gunner(bot))
