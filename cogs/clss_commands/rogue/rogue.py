import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class rogue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 stabs usr2 in the bdypart.",
            "usr1 sneaks up on usr2, stabbing them in the bdypart.",
            f"usr1 walks up to usr2, then stabs them a total of {random.randint(2,20)} times in the bdypart. Yeah, I think that'll do it.",
            "usr1 throws one knife into usr2's bdypart, then runs up and slits their throat. Brutal, man! Brutal!",
            "usr1 sneaks up behind usr2 and stabs them, ending them quickly.",
            "usr1 stabs usr2 28 times. 28 stab wounds!",
            "usr1 surgically removes usr2's bdypart. Well, maybe not *surgically*, but you get the idea.",
            "usr1 slowly pushes their knife into usr2's bdypart. usr1 smiles evilly.",
            "usr1 is in need of bdypart. usr2 happens to have bdypart. You know where this goes.",
            f"usr1 stands across from usr2. A standoff. usr1 smiles, revealing the contents of their trenchcoat. It's... knives. To be exact, it's {random.randint(10,200)} knives. usr1 throws each and every knife at usr2. Lets just say, usr2 didn't make it out.",
            "usr1 is out at a romantic dinner with usr2. usr1 waits until no one is looking, then grabs the butterknife, cutting out usr2's bdypart, and making a dash for it.",
            "usr1 cuts off usr2's bdypart.",
            "usr1 stabs usr2.",
            "usr1 leaps onto usr2's back, then plunges their knives into usr2's chest. FATALITY!",
            "usr1 feels a sudden onset of bloodlust. Unfortunately, usr2 is the closest person. usr1 is now the proud owner of usr2's bdypart.",
            "usr1 stands across from usr2.\n\n'Do you really think you can stop me?' laughs usr1.\n\n'Ha! You overestimate your own power' says usr2.\n\nusr2 attacks usr1, but in the blink of an eye, usr1 is behind usr2. \n\n'I'm going to cut out your bdypart, stuff it, and put it on my mantle.'\n\nusr2 is struck with fear as usr1 stabs them. usr1 smiles evilly. The deed is done."
        ]

        self.hooks_c = [
            "usr1 cuts out usr2's bdypart while they're asleep, and sells it on the black market for 50$.",
            "usr1 breaks into usr2's home and stabs them in the bdypart.",
            "usr1 sneaks into usr2's home, yoinks some valuables, then suffocates usr2 with a pillow.",
            "usr1 stabs usr2 in an alleyway and steals their wallet. Yoink!",
            "usr1 stabs usr2 on their way back home, then steals their purse.",
            "usr1 shanks usr2 in the back and runs away.",
            "usr1 kicks usr2 in front of an oncomming train.",
            "usr1 stabs usr2 in the bdypart, then steals their kidneys.",
            "usr1 stabs usr2 with a pencil in a bar, then robs the bar and runs away.",
            "usr1 tricks usr2 into giving them their credit card information, then stabs them in the bdypart.",
            "usr1 chases usr2 down the street then chloroforms them before stabbing them.",
            "usr1 follows usr2 to their car and sneaks into the trunk. Once usr2 arrives home, usr1 jumps out and stabs them before stealing their car.",
            "usr1 pretends to be a homeless guy and scams usr2. Oh, then stabs them. Like 15 times. It was a bit unnecessary, really."
        ]

        self.hooks_t = [
            "usr1 cons usr2 with a really obviously fake story. C'mon, usr2, you're smarter than this!",
            "usr1 stabs usr2 in the neck and takes their wallet.",
            "usr1 jumps usr2 in the alley and takes their lunch money!",
            "usr1 knocks usr2 out, extracts their bdypart, and sells it on the black market.",
            "usr1 kicks usr2 in the stomach before taking the cash from usr2's back pocket, and running.",
            "usr2 is walking home when they realise their wallet is missing! usr1 hides in a bush, holding usr2's wallet, and chuckles.",
            "usr1 throws pocket sand into usr2's eyes and steals their bdypart. Aw snap!",
            "usr1 trips usr2 and steals their credit card information. Time for vbucks!",
            "usr1 kicks usr2 into a wall, stabs them, and steals their pants. Damn, that sucks."
        ]
    
        self.hooks_n = [
            "usr1 throws sand at usr2, then throws their scimitar at them.",
            "usr1 kicks usr2 into a cactus. Owch!",
            "usr1 throws a cactus into usr2's bdypart. Rude.",
            "usr1 fights usr2 for a while before delivering the killing blow to their bdypart. Fatality!",
            "usr1 kicks some sand up at usr2 before stabbing them through the bdypart. Rough.",
            "usr1 drops a house on usr2. What? Isn't that what Nomads do?",
            "usr1 throws their scimitar through usr2's bdypart. Owch!",
            "usr1 trips usr2, then plunges their scimitar into their bdypart."
        ]

        # Homes for the Nomad class.
        self.nomad_homes = {}

        self.hooks_scav = [
            "usr1 throws scrap metal at usr2's bdypart, impaling it! Owch!",
            "usr1 trips usr2 then drops a boom bot on them. Kaboom!",
            "usr1 slashes usr2 with a scrap sword. If that doesn't kill them, the tetanus will!",
            "usr1 throws scrap through usr2, piercing their bdypart!",
            "usr1 kicks usr2 into a pit of rusty spikes. Damn, that's gotta hurt.",
            "usr1 throws a boom bot under usr2, blowing them sky high!",
            "usr1 throws a bunch of scrap caltrops below usr2, then slices their legs off so they fall into it. Ow!",
            "usr2 is walking down the street when all of a sudden, they see a Fredster! Encapsulated by the Fredster, they fail to notice usr1 sneaking up on them before it's too late! usr1 stabs them through the bdypart!"
        ]

        self.wanderer_chan = {}

        self.hooks_wander = [
            "usr1 throws a knife into usr2, then kicks it deeper with a dropkick. Ouch!"
        ]

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def shank(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "rogue":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL BACKSTAB]✨** + 125 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 125)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "criminal":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_c)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "thief":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_t)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        steal_chance = random.randint(1,10)
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook

                        if steal_chance == 1:
                            try:
                                async with aiosqlite.connect('main.db') as conn:
                                    async with conn.execute(f"select item_name from inventory where uid = {target.id};") as chan:
                                        stuff = await chan.fetchall()

                                stolen_item = random.choice(stuff[0])
                                
                                await h.remove_items(target.id, self.bot, stolen_item, 1)
                                await h.alter_items(ctx.author.id, ctx, self.bot, stolen_item, change = 1)
                                hook += f"\n\n*{ctx.author.display_name} steals {target.display_name}'s **{stolen_item}**!*"
                            except IndexError:
                                pass
                        else:
                            await h.add_gold(ctx.author.id, 200, self.bot)
                            try:
                                await h.add_gold(target.id, -200, self.bot)
                                hook += f"\n\n*{ctx.author.display_name} steals 200 gold from {target.display_name}!*"
                            except TypeError:
                                hook += f"\n\n*{ctx.author.display_name} gives 200 gold to {target.display_name}, then instantly steals it!*"

                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "nomad": 
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    if ctx.author in self.nomad_homes.keys():
                        if self.nomad_homes[ctx.author] == ctx.channel:
                            boost = 9
                        else:
                            boost = 0
                    else:
                        boost = 0

                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel, boost)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_n)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        if ctx.author in self.nomad_homes.keys() or ctx.channel in self.nomad_homes.values():
                            hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        else:
                            hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook + f"\n\n*🚩 | **{ctx.author.display_name}** claims this channel as their home!*"
                            self.nomad_homes[ctx.author] = ctx.channel
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "scavenger":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_scav)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness, + 1 *Scrap* | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await h.alter_items(ctx.author.id, ctx, self.bot, "scrap", 1)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "wanderer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_wander)
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
    bot.add_cog(rogue(bot))
