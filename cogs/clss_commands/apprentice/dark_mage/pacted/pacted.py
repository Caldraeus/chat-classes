import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
from sqlite3 import OperationalError

"""
INFO:
Uses ;attack, which is actually under Tamer.py
The rest of the commands, ;invoke and ;demon are here.
"""

class pacted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users_demons = {}
        self.demons_small = {
            "sugollix" : "https://i.pinimg.com/originals/f7/bf/8e/f7bf8ebeb031a970efe05cccdbc739cb.jpg",
            "ilixnith" : "https://lh3.googleusercontent.com/proxy/KQjzFG9dcK0U-CKji_ZDotezNC0Ut446T2iAdimJeimokPeeRbl-2gh8gRcApqOVsstPPOAa48htOggVxLe-r8Y1izd9U_37vXVNr46hbHv75e9uhKyNj1ZwAq55jvzSqWZpnu5Vj9diYmsRATDh7sdxthgKHhEunpA",
            "foop" : "https://i.pinimg.com/originals/96/82/c5/9682c58dc4263dcfc9229c1c6747cc47.jpg",
            "trokgroor" : "https://gbf.wiki/images/thumb/f/f1/Summon_b_2030018000.png/408px-Summon_b_2030018000.png",
            "zollok" : "https://cdn.dribbble.com/users/537078/screenshots/11366007/media/352aea10a6fcb860a5e6f3bbd5b6e715.gif",
            "malakar" : "https://i.pinimg.com/736x/b7/8f/5b/b78f5b8cbdf2ec339a035c67b1a15dbe.jpg",
            "minehart" : "https://i.pinimg.com/originals/63/2b/07/632b079977fd041db073d7c82ec2691c.jpg"
        }
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

    @commands.command()
    @commands.guild_only()
    async def demon(self, ctx): # Shoots an arrow at someone.
        uid = ctx.author.id
        if uid in self.users_demons:
            demon = self.users_demons[uid]
        else:
            async with aiosqlite.connect('classTables.db') as conn:
                async with conn.execute(f"select uid, demon from pacted_demons where uid = '{uid}'") as u_info:
                    user_info = await u_info.fetchone()
            if user_info:
                pass
            else:
                profile = discord.Embed(title=f"Annaisha's Totally Legal Demons!", colour=discord.Colour.from_rgb(255, 165, 0))
                profile.add_field(name="Sugollix", value="A lustful demon capable of producing a healing liquid! Lets you heal people like a healer would!", inline=False)
                profile.add_field(name="Ilixnith", value="A wrathful demon capable of fighting for long periods of time! Your criticals give you 2.5x coolness!", inline=False)
                profile.add_field(name="Foop", value="A gluttonous demon made of a green goo! Your hot dogs are buffed!", inline=False)
                profile.add_field(name="Trokgroor", value="A greedy demon, raised from a fallen king! You gain 5x daily gold!", inline=False)
                profile.add_field(name="Zollok", value="A slothful demon, who always seems to be asleep! The longer you don't get a crit, the more your next crit does!", inline=False)
                profile.add_field(name="Malakar", value="A prideful demon, they never shut up! Allows you to `;gloat`, which gives you a stack of confidence, increasing your critical chance!", inline=False)
                profile.add_field(name="Minehart", value="A envious demon, always looking around for others! Whenever someone gets a critical on you, Minehart saves a % of the coolness for you to gain with `;invoke`!", inline=False)
                await ctx.send("You have no demon yet! Here, let me grab you some...! Here, I have the following fledgling demons!", embed=profile)
        
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(pacted(bot))
