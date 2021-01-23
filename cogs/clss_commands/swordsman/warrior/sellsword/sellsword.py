import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
import time

class sellsword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 heaves their sword into usr2, completely removing their bdypart. Ouch!",
            "usr1 charges at usr2, impaling usr2 upon their sword.",
            "usr1 stands across from usr2.\n\n'So, it comes to this, does it?'\n\nusr1 smiles. 'I always knew it would.'\n\n'I guess we'll never be able to go on that fishing trip, huh?'\n\n'Yeah, I guess not.'\n\nusr1 raises their sword, and with one decisive strike, removes usr2's bdypart. They fall over, dead. usr1 wipes tears off of their face as they walk away.",
            "usr1 heaves their sword into usr2's bdypart. Damn!",
            "usr1 blocks usr2's first attack, then flips them over using their shield. usr1 then follows that up with a plunging attack into usr2's bdypart.",
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
        self.hired = {}

    pass

    @commands.command()
    @commands.guild_only()
    async def hire(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target.id != 713506775424565370:
            user_hired = target.id
            if self.bot.users_classes[str(user_hired)] == "sellsword" and user_hired != ctx.author.id:
                if user_hired in self.hired:
                    await ctx.send("This sellsword has already been hired for the day!")
                elif ctx.author.id in list(self.hired.values()):
                    await ctx.send("You have already hired a sellsword for the day!")
                else:
                    await ctx.send(f"{ctx.author.mention} : Are you sure you want to hire {target.mention} until rollover? It will cost 200 G.\n\n`1. Yes\n2. No`")
                    def check(m: discord.Message):
                        return m.content and m.channel == ctx.message.channel and m.author == ctx.message.author

                    try:
                        chosen = await self.bot.wait_for('message', check=check, timeout=30)

                        if (chosen.content.lower() == "yes" or chosen.content == "1") and str(ctx.author.id) in self.bot.users_classes:
                            await h.add_gold(ctx.author.id, -200, self.bot, purchase_mode = ctx)
                            await h.add_gold(target.id, 200, self.bot)
                            self.hired[user_hired] = ctx.author.id
                            await ctx.send(f"<:check_yes:802233343704956968> | You have hired {target.mention} for the rest of the day! They will get 100 coolness every time you are attacked!")
                        else:
                            await ctx.send("Transaction cancelled.")
                    except SyntaxError:
                        pass
                    
                      
# A setup function the every cog has
def setup(bot):
    bot.add_cog(sellsword(bot))
