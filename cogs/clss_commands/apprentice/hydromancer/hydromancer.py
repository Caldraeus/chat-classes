import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class hydromancer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 blasts usr2 with a beam of water.",
            "usr1 fires water bubbles at usr2.",
            "usr1 creates a whirlpool around usr2, carrying them far, far away.",
            "usr1 creates a blade of water, cutting off usr2's bdypart!",
            "usr1 creates tentacles of water, piercing usr2's bdypart. Ew.",
            "usr1 creates a gargantuan wave, engulfing usr2 and drowning them.",
            "usr2 attacks usr1, but usr2 blocks it with a wall of water, which then collapses in on usr2, killing them!",
            "usr1 shoots a jet of water through usr2's bdypart! It's super effective!"
        ]

        self.waterlevels = {}
    pass

    @commands.command()
    @commands.guild_only()
    async def douse(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "hydromancer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works:
                    if ctx.author.id not in self.waterlevels:
                        self.waterlevels[ctx.author.id] = 0
                    elif ctx.author.id in self.waterlevels:
                        self.waterlevels[ctx.author.id] += random.randint(0,20)

                    hook = random.choice(self.hooks)
                    crit_check = random.randint(1,20)

                    waterlevels = self.waterlevels
                    if waterlevels[ctx.author.id] <= 25:
                        hook += f"\n\n*usr1's water level sits lowly at {waterlevels[ctx.author.id]}%.*"
                    elif waterlevels[ctx.author.id] <= 50:
                        hook += f"\n\n*usr1's water level sits comfortably at {waterlevels[ctx.author.id]}%.*"
                    elif waterlevels[ctx.author.id] <= 75:
                        hook += f"\n\n*usr1's water level sits highly at {waterlevels[ctx.author.id]}%.*"
                    elif waterlevels[ctx.author.id] <= 99:
                        hook += f"\n\n*usr1's water level is close to overflowing at {waterlevels[ctx.author.id]}%!*"
                    elif waterlevels[ctx.author.id] >= 100:
                        crit_check = 100
                        waterlevels[ctx.author.id] = 0

                    body_part = random.choice(h.body_parts)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    
                    if crit_check < 20:
                        await ctx.send(hook)
                    elif crit_check == 20:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    elif crit_check == 100:
                        hook = "**💧[OVERFLOW]💧** + 5 AP | " + hook

                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 6
                        self.bot.users_ap[str(ctx.author.id)] = new_ap

                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(hydromancer(bot))
