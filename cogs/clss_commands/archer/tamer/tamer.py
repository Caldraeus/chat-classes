import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class tamer(commands.Cog): # Yasha : Falcon
                           # Ursol : Bear
                           # Rolph : Wolf
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 invokes Yasha the Falcon, causing her to fly down and scratch at usr2's bdypart!",
            "usr1 and Rolph the Wolf track down usr2, before putting an end to them.",
            "usr1 rides Ursol the Bear into battle against usr2, eaily beating them with Ursol's help.",
            "usr2 is running away from usr1, when they hear a whistle. All of a sudden, Rolph the Wolf jumps out from the underbrush and sinks his teeth into usr2's bdypart. Ouch!",
            "usr1 invokes Yasha the Falcon to find usr2. Yasha reports back to usr1, who then quietly sneaks into usr2's house and assassinates them.",
            "usr1 is playing fetch with Rolph the Wolf when usr2 attempts to attack usr1. Rolph makes quick work of usr2, bringing usr1 back some of usr2's stuff as a toy.",
            "usr1 is enjoying some tea with Ursol the Bear when usr2 rudely interrupts. Ursol roars and slashes usr2 in the bdypart, which falls out onto the floor.",
            "usr1 is spending some time with their animal companions when usr2 tries to assassinate usr1. usr2 fails, and all three animal companions turn to look at usr2. Needless to say, usr2 is reduced to a fine red paste.",
            "usr1 invokes Rolph the Wolf, sending him after usr2. usr2 is able to fend off Rolph, but backs up into usr1, who uses a woodland dagger to stab them in the back.",
            "usr1 invokes Ursol the Bear and sends him to usr2. usr2 tries to fight Ursol, but is no match for the mighty bear.",
            "usr1 has Yasha the Falcon dive into usr2's face, taking their eyes out, before Ursol the Bear finishes usr2 with a mighty strike.",
            "usr1 invoke Rolph the Wolf and Ursol the Bear to find usr2. usr2 is minding their business when a large wolf and bear come out of the woods. urs2 tries to run away, but it is futile.",
            "usr1 commands all three animal companions to tear usr2 apart, limb from limb. Ouch!",
            "usr1 commands all animal companions to attack usr2, then feeds them all usr2's bdypart."
        ]
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def attack(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "tamer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(tamer(bot))
