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
            "usr2 attacks usr1, but usr1 blocks it with a wall of water, which then collapses in on usr2, killing them!",
            "usr1 shoots a jet of water through usr2's bdypart! It's super effective!",
            "usr1 slams their hand against usr2's face, then drowns them by creating a constant stream of water! Brutal, man!",
            "usr1 meets usr2 on a beach. Their goal? To duel.\n\n'You stand no chance. I'm not an apprentice anymore, usr2.'\n\n'Heh. I'm sure.'\n\nusr1 then causes the ocean water to their left to rise up, up, and create a giant fist of water. usr2's eyes go wide, as they realise they have lost. The fist comes down, crushing usr2 to a pulp.",
            "usr1 shoots usr2 with a squirtgun. Then shoots them with a extremely powerful blast of water, causing their bdypart to fly out.",
            "usr1 pulls all of the liquid out of usr2, causing them to shrivel up. Ew, but cool!",
            "usr1 swells usr2's bdypart with water, causing it to burst! usr2 drops, dead.",
            "usr2 is swimming when all of a sudden the ocean begins to churn. usr1 floats from below the sea, then smiles - evily. usr2 goes wide eyed as the ocean pulls them deep under, drowning them. Spooky!",
            "usr1 uses a swell of water to push a bunch of debris into usr2, crushing them!",
            "usr1 shoots three arrows of water into usr2's bdypart, obliterating it.",
            "usr1 shoots a beam of powerful water at usr2, slicing off their bdypart, leg, arm and finally cutting them in half! Brutal!"
        ]

        self.waterlevels = {}
    pass

    @commands.command()
    @commands.guild_only()
    async def douse(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "hydromancer" or self.bot.users_classes[str(ctx.author.id)] == "multi-mage":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx): 
                    if ctx.author.id not in self.waterlevels:
                        self.waterlevels[ctx.author.id] = 0
                    elif ctx.author.id in self.waterlevels:
                        self.waterlevels[ctx.author.id] += random.randint(0,20)

                    hook = random.choice(self.hooks)
                    crit_check = 0

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

                    if crit_check != 100:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)

                    body_part = random.choice(h.body_parts)
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
                        hook = "**💧[OVERFLOW]💧** + 5 AP | " + hook

                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 6
                        self.bot.users_ap[str(ctx.author.id)] = new_ap

                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "tidal mage" and await h.can_attack(ctx.author.id, target.id, ctx):
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author.id not in self.waterlevels:
                        self.waterlevels[ctx.author.id] = 0
                    elif ctx.author.id in self.waterlevels:
                        self.waterlevels[ctx.author.id] += random.randint(15,40)

                    hook = random.choice(self.hooks)
                    crit_check = 0

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

                    if crit_check != 100:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    
                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
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
