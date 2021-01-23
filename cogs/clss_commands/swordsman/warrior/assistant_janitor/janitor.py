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
from better_profanity import profanity
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

class janitor(commands.Cog):
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
        profanity.load_censor_words()
    pass

    @commands.command()
    @commands.guild_only()
    async def clean(self, ctx): # Shoots an arrow at someone.
        if self.bot.users_classes[str(ctx.author.id)] == "assistant janitor":
            ap_works = await h.alter_ap(ctx.message, 1, self.bot)
            
            if ap_works:
                messages = await ctx.channel.history(limit=2).flatten()
                message_checking = messages[1]
                author = message_checking.author
                if profanity.contains_profanity(message_checking.content):
                    if message_checking.author != ctx.author:
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(ctx.channel)
                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await hook.send(content=profanity.censor(message_checking.content, "○"), username=author.display_name, avatar_url=author.avatar_url)
                        await message_checking.delete()
                        await messages[0].delete()
                        await h.add_coolness(ctx.author.id, 1000)
                        await h.add_gold(ctx.author.id, 500, self.bot)
                    else:
                        await ctx.send("You can't clean your own message! Also, for even trying this, I'm taking away 100 coolness from you for swearing!")
                        await h.add_coolness(ctx.author.id, -100)
                else:
                    await ctx.send(f"{ctx.author.mention} | Previous message contains no obvious profanity!")
                    
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(janitor(bot))
