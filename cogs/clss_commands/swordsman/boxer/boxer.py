import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class boxer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 pummels usr2 to death.",
            "usr1 swings a fist right into usr2's bdypart, causing them to double over. usr1 then slams their head into the ground.",
            "usr1 throws three jabs at usr2, then finishes with a left hook into usr2's head.",
            "usr1 releases an uppercut into usr2, sending them flying before slamming back into the ground.",
            "usr1 throws a powerful bolo punch at usr2. usr2, never having seen a bolo punch, takes the full force to the head and instantly passes out.",
            "usr1 throws a jab, an uppercut, a left hook, an overhand right and finally a finishing blow straight into usr2's bdypart. A full combo!",
            "usr1 weaves around usr2's attack then smashes them in the face with their bare hands.",
            "usr1 grapples usr2, throwing them to the side and releasing several strong punches.",
            "usr1 catches usr2 off guard, slamming a fist straight through usr2's bdypart, obliterating it in an instant.",
            "usr1 throws a light jab into usr2, then kicks their knee inward and finishes them with an uppercut.",
            "usr1 punches usr2 in the bdypart, then then face, then kicks them into a wall to finish them.",
            "usr1 tackles usr2 and beats them to death."
        ]

    pass

    @commands.command()
    @commands.guild_only()
    async def punch(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "boxer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):

                    hook = random.choice(self.hooks)
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    
                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
                        if str(target.id) in self.bot.users_ap.keys():
                            new_ap = self.bot.users_ap[str(target.id)] - 2
                            if new_ap < 0:
                                new_ap = 0

                            self.bot.users_ap[str(target.id)] = new_ap

                        hook = "**🥊[KNOCKOUT]🥊** + 100 Coolness | " + hook + f"\n\n***{target.display_name}** loses 5 AP from the beating!*"
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(boxer(bot))
