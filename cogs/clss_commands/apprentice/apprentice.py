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
            "usr1 blinds usr2 with magic, then fires a shadowbolt through their bdypart!",
            "usr1 stabs usr2 with a ritual dagger, then pulls their blood out using magic.",
            "usr1 causes usr2's bdypart to slowly decay. It doesn't even kill them, it's just kinda rude.",
            "usr1 collects some minor souls to haunt usr2. usr2 begs for mercy after a day of haunting, and usr1 steals their soul.",
            "usr1 contorts usr2's bones, then steals their bdypart.",
            "usr1 melts usr2's insides, then extracts their bones.",
            "usr1 teleports usr2 to the seventh layer of hell. Have a good one!",
            "usr1 extracts usr2's bdypart before turning them into a fine red paste.",
            "usr1 uses magic to crush usr2's heart, instantly killing them.",
            "usr1 torments usr2 with shadows before finally tearing out their bdypart.",
            "usr1 pays a demon to kill usr2. usr2 is last seen entering their home, then never seen again. Thanks, Illxylnth!",
            "usr1 clouds usr2's mind with horrible images, causing usr2 to jump into the nearest volcano.",
            "usr1 magically manipulates a needle to pierce usr2's bdypart several times, then lodge into their brain.",
            "usr1 follows usr2 home, then invades their dream, killing them in their nightmare and in the real world at the same time.",
            "usr1 tears usr2 apart limb by limb with the help of some imps.",
            "usr1 causes usr2 to go insane and rip out their own bdypart.",
            "usr1 inverts usr2. Which, as I'm sure you can imagine, is really, really nasty. And messy.",
            f"usr1 swaps usr2's bdypart and {random.choice(h.body_parts)} in their sleep. Huh."
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def blast(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370 and await h.can_attack(ctx.author.id, target.id):
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
