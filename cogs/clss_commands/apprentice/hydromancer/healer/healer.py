import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class healer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 heals usr2's bdypart injury",
            "usr1 rushes over to usr2 and casts a healing spell on them",
            "usr1 pulls out an arrow from usr2's bdypart, then heals the wound",
            "usr1 heals usr2 in the midst of battle",
            "usr1 heals usr2's broken bdypart",
            "usr1 surrounds usr2 in a healing water, bringing them back to full health",
            "usr1 drags usr2 to safety and heals them back up",
            "usr1 reattaches usr2's bdypart properly"
        ]
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def heal(self, ctx, target: discord.Member = None): 
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "healer":
                ap_works = await h.alter_ap(ctx.message, 3, self.bot)
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
                        ap_healed = random.randint(1,10)
                        new_ap = self.bot.users_ap[str(target.id)] + ap_healed
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(target.id)] = new_ap
                    
                    await h.add_coolness(ctx.author.id, 50*ap_healed)

                    await ctx.send(f"{hook}, restoring {ap_healed} AP to them and personally gaining {ap_healed*50} coolness!")
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(healer(bot))
