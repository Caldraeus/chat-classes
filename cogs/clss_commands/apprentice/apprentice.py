import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class apprentice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 blasts usr2.",
            "usr1 blasts usr2 with a fireball, burning away their bdypart.",
            "usr1 fires an arcane beam into usr2's bdypart! Goodbye, bdypart!",
            "usr1 is practicing their magic when usr2 walks across the firing range. The only thing left is a pile of dust and usr2's bdypart.",
            "usr1 creates a blizzard, completely freezing usr2.",
            "usr1 beats usr2 to death with their spellbook.",
            "usr1 stands across from usr2.\n\n'So, usr2... we meet again.'\n\n'So it seems.'\n\n'I've been practicing. All this time, day after day. You stand no chance.'\n\nusr2 laughs. 'Yeah, I bet.'\n\nusr1 then focuses their magic to summon a giant spike constructed of earth. usr2's eyes go wide. They begin to run. It is futile. usr1's shard of earth slams into usr2, completely obliterating them. usr1 smiles. They did it.",
            f"usr1 shoots {random.randint(2,50)} shards of thin ice into usr2's bdypart. They collapse, dead.",
            "usr1 traps usr2 in a stone sphere, then rolls them into a volcano. Bye bye!",
            "usr1 strikes usr2 with lighting. Zap!",
            "usr1 shoots a blast of fire at usr2, setting their bdypart on fire. Hot!",
            "usr1 summons a wave of magic and cuts usr2 in half. Easy weightloss!",
            "usr1 summons a block of ice above usr2, then lets it fall. Lets just say, usr2 is a lot thinner than before.",
            "usr1 shoots a beam of light through usr2's bdypart. Precision!",
            "usr2 runs at usr1, but usr1 summons a wall of ice spikes right in front of them. Splat!",
            "usr1 teleports usr2 into the earth's core.",
            "usr1 teleports usr2 into the air, then fires 3 pyroblasts at them. usr2's bdypart, liver, and intestines rain down from the sky. Fireworks!",
            "usr1 teleports inside of usr2, then breaks through them. Brutal!",
            "usr1 fires several fireballs at usr2, striking them in the bdypart."
        ]
        self.hooks_dm = [
            "usr1 blinds usr2 with magic, then fires a shadowbolt through their bdypart!"
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def blast(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "apprentice":
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
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "dark mage":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works:
                    crit_check = random.randint(1,20)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_dm)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check != 20:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(apprentice(bot))
