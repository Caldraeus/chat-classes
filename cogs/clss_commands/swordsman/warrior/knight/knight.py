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

class knight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1’s horse stomps usr2 to death with its hooves.",
            "usr1 removes usr2’s bdypart with a single swing. “Just a flesh wound!” they proclaim.\n\nWell, it is definitely more than a flesh wound.",
            "usr1 throws a coconut at usr2. It bonks off their bdypart with an extremely undignified sound.",
            "usr1 charges usr2 on horseback, impaling their lance through their bdypart.",
            "usr1 grips their sword by the blade and beats usr2 to death with the hilt.",
            "usr1 cuts down usr2 with their sword, then stops to offer a prayer for their soul.",
            "usr1 charges across an open field at usr2. For nearly a minute, tense drums echo from the ether, the brave knight appearing to get no closer, so great is the distance between them. Then, with frankly improbable speed, the final gap is closed! usr2 is stabbed in the bdypart! Which sucks, but at least now they don’t have to go to that stupid wedding.",
            "usr2 blows rain down upon usr1, but their armor is impenetrable. Their sword lashes out once in retaliation, taking usr2’s bdypart and ending the duel.",
            "usr1 throws down their gauntlet, demanding an honorable duel! Then, when usr2 bends down to pick it up, they stab them in the bdypart from behind. Honorably.",
            "The light reflecting off of usr1’s shining armor blinds usr2, leaving them open to a strike that cuts off their bdypart.",
            "usr1 unscrews the pommel of their sword, and tosses it into the skull of usr2, ending them rightly."
        ]
        self.crusade = None

    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def slash(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "knight":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if self.crusade != None:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id, 9)
                        if str(crusade[1]) == str(crusade[2]):
                            self.crusade = None
                    else:
                        crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        crusade_chance = random.randint(1,8)
                        if crusade_chance == 1 and self.crusade == None:
                            og_time = time.strftime("%H:%M")
                            end_time = og_time.split(":")
                            end_time[0] = str(int(end_time[0]) + 2)
                            if int(end_time[0]) > 24:
                                end_time[0] = str(int(end_time[0]) - 24)
                            end_time = ':'.join(end_time)

                            self.crusade = [ctx.author.name, og_time, end_time]
                            hook += "\n\n*🚩 | You have started a crusade!*"
                            
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)

    @commands.command()
    @commands.guild_only()
    async def crusade(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if self.bot.users_classes[str(ctx.author.id)] == "knight":
            if self.crusade != None:
                await ctx.send(f"**Crusade** is active! This crusade was started by {self.crusade[0]} at `{self.crusade[1]}` and will end at `{self.crusade[2]}` (EST).")
            else:
                await ctx.send("No active crusade. The holy lands are safe, for now.")
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(knight(bot))
