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

        self.hooks_cryo = [
            "usr1 flings a shard of ice straight through usr2's bdypart!",
            "usr1 freezes usr2's arm before shattering it with a punch.",
            "usr1 shoves a large icicle through usr2's bdypart!",
            "usr1 freezes usr2's bdypart before ripping it out and smashing it on the ground.",
            "usr1 creates a patch of ice below usr2, causing them to slip and fall. It doesn't kill them or anything, it's just kinda funny.",
            "usr2 is minding their own business when they're suddenly unable to move. Their legs have been frozen! They looks behind them to see usr1 sliding at them in a sled! By the time they break free it's too late - usr1 smashes through usr2 at mach speed.",
            "usr1 throws a snowball into usr2's face before brutally stabbing them to death with blades of ice.",
            "usr1 creates a scythe of ice and swipes usr2's head off!",
            "usr1 freezes usr2's brain, slowly killing them.",
            "usr1 slams into the earth, causing shards of ice to rise up beneath usr2, impaling them!",
            "usr1 covers themself in ice and tackles usr2, crushing them!",
            "usr1 freezes usr2's fingers, and breaks them. One. By. One. That's just cruel, usr1. Just cruel."
        ]
        self.impaled = []

        self.hooks_fog = [
            "usr1 surrounds usr2 in mist, then uses it to choke them to death!",
            "usr1 uses the fog to slice at usr2, cutting off their bdypart!",
            "usr1 causes usr2 to get lost in a forest due to the fog. usr2 is never seen again.",
            "usr1 whips wind at usr2, shredding their bdypart!",
            "usr1 pushes usr2 off a cliff using a fist of fog.",
            "usr1 creates a wall of fog in front of usr2, and another behind them. Then, usr1 slams the two walls together, smushing usr2. That was... a bit intense.",
            "usr1 forces thick fog down usr2's orfices, causing them to vomit up blood and die. Holy shit. A bit much usr1, don't you think?",
            "usr1 causes a thick fog to encapsulate usr2, then lifts them far, far away. Bye bye!"
        ]

        self.hooks_psychic = [
            "usr1 lifts usr2 with their telekinesis, then rips them in two!",
            "usr1 mind controls usr2 to jump off a cliff! Brutal!",
            "usr1 causes usr2's bdypart to pop.",
            "usr1 twists usr2's body, demolishing their insides.",
            "usr1 reads usr2's mind and causes usr2 to see their biggest fear: the opposite gender. It's so scary, usr2 drops dead.",
            "usr1 lifts a car up using their mind and slams it onto usr2.",
            "usr1 shoots psychic bolts at usr2, piercing their bdypart and killing them!",
            "usr1 flattens usr2 with a burst of psychic energy!",
            "usr1 causes usr2's organs to suddenly rupture. usr2 drops, dead."
        ]

        self.hooks_sorc = [
            "usr1 blasts usr2 apart with lava!",
            "usr1 shoots an arcane orb through usr2, ripping them in two!",
            "usr1 slams the ground, releasing an arcane shockwave that turns usr2 to dust!",
            "usr1 fires an arcane missile at usr2, blowing off their bdypary. usr1 then runs up to usr2 and slams them into the ground, before blasting them at point blank with a fireball.",
            "usr1 shoots two bolts of crackling energy into usr2's legs, crippling them.",
            "usr1 rips out usr2's bdypart, sets it on fire, then fires it back at usr2.",
            "usr1 shocks usr2, completely frying them.",
            "usr1 fires raw magical energy into usr2's bdypart, causing it to explode.",
            "usr1 makes a huge orb of magical energy, and slams it into usr2, completely destroying them!",
            "usr1 shoots out three discs of magic, slicing off usr2's bdypart, arm and both legs! Fatality!",
            "usr1 kicks usr2 off a bridge, then fires a beam of magic through them as they fall down!",
            "usr1 sets usr2 ablaze in a spectacular blue flame. usr2 runs around in circles before burning to death."
        ]

        self.hooks_toxin = [ 
            "usr1 fires globs of poison at usr2, dissolving their flesh!",
            "usr1 pricks usr2 with a needle, poisoning them to death.",
            "usr1 summons poisonous mushrooms in usr2's lungs, killing them slowly.",
            "usr1 fires a wave of poison at usr2, dissolving their flesh and killing them, slowly.",
            "usr1 slams into usr2, then turns their blood to poison, killing them painfully.",
            "usr1 charges up a massize ball of energy, then fires out a smog of poison around usr2. usr2 coughs, trying to escape, but ultimately dies in the smog.",
            "usr1 dodges usr2's attack, then puts their hand over usr2's mouth before summoning a ton of poison, killing them.",
            "usr1 flings poison into usr2's eyes, causing them to bleed and dissolve, killing usr2. Brutal!",
            "usr1 jabs usr2 in the neck with a vial of poison. usr2's neck dissolves, and they die.",
            "usr1 fires four magical poison bolts into usr2's bdypart, poisoning it badly and causing the poison to spread out among the rest of usr2, killing them.",
            "usr1 poisons usr2 badly, then watches usr2 flail about as they die. Painfully. Slowly.",
            "usr1 forces poison into usr2's bdypart, then watches it slowly dissolve."
        ]

        self.souls = {}

        self.hooks_crusher = [
            "usr1 fires a blast into usr2, ripping their soul apart.",
            "usr1 grabs usr2 and drains their life essence.",
            "usr1 grabs usr2's bdypart and tears it off, before crushing it and punching usr2.",
            "usr1 slams their staff into usr2, then fires off multiple magic blasts. Ouch!",
            "usr1 kicks usr2 back, then tears their soul out and pockets it.",
            "usr1 grabs usr2 and tears out their soul, before curbstomping it. Damn, dude.",
            "usr1 fires multiple blasts into usr2, demolishing them.",
            "usr1 grabs usr2 and slams them into the ground, then tears out usr2's soul.",
            "usr1 kicks usr2 into the wall, then forcefully seperates their soul from their body.",
            "usr1 throws usr2 into the ground and blasts a hole through their bdypart."
        ]

        self.hooks_pact = [
            "usr1 shoots a dark blast of energy at usr2!",
            "usr1 has their demon rip out usr2's bdypart!",
            "usr1 removes usr2's bdypart and feeds it to their demon! Awwww.",
            "usr1 throws their demon at usr2, who rips apart usr2.",
            "usr1 blasts usr2's bdypart off, then has their demon rip apart usr2.",
            "usr1's demon trips usr2, then usr1 fires a dark blast through usr2. Team work makes the dream work!",
            "usr1's demon jumps on usr2, causing usr2 to trip and fall into a nearby river and drown. Huh, okay.",
            "usr1 blasts usr2 in the stomach, causing blood to drip out. usr1's demon quickly runs over and drinks usr2's blood. Ewww!!",
            "usr1 blasts usr2 in the bdypart, then leaves the rest to their demon.",
            "usr2 is minding their own business when they see usr1's demon! usr1's demon makes short work of usr2, then reports back to usr1! High five!",
            "usr1's demon blocks an attack from usr2, then usr1 follows up with a blast into usr2's bdypart!"
        ]

        self.zollok = {}
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def blast(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "apprentice":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "dark mage":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_dm)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "cryomancer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_cryo)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if target.id not in self.impaled:
                        if crit_check == False:
                            await ctx.send(hook)
                        else:
                            self.impaled.append(target.id)
                            hook = "**<:icicle:790043249456840734>[IMPALEMENT!]<:icicle:790043249456840734>** + 100 Coolness | " + hook
                            await h.add_coolness(ctx.author.id, 100)
                            await ctx.send(hook)
                    else:
                        chance_to_stay = random.randint(1,3)
                        hook = "**✨[MINI-CRIT]✨** + 75 Coolness | " + hook
                        if chance_to_stay == 1:
                            hook += "\n*The icicle stays lodged!*"
                        else:
                            self.impaled.remove(target.id)
                        
                        await h.add_coolness(ctx.author.id, 75)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "fogwalker":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_fog)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        if ctx.author.id in self.bot.server_boosters: # Check their maximum AP
                            max_ap = 40
                        else:
                            max_ap = 20

                        if str(ctx.author.id) in self.bot.users_ap:
                            new_ap = self.bot.users_ap[str(ctx.author.id)] + 10
                            if new_ap > max_ap:
                                new_ap = max_ap
                            self.bot.users_ap[str(ctx.author.id)] = new_ap
                        hook = "**🌫️[CRITICAL]🌫️** + 100 Coolness, + 10 AP | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "psychic":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_psychic)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**⛓️[MINDSHATTER]⛓️** + 100 Coolness | " + hook + " This is so mind-destroying that it applies 5 stacks of **shatter** to them!"
                        await h.add_coolness(ctx.author.id, 100)
                        await h.add_effect(target, self.bot, "shatter", 5)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "sorcerer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_sorc)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook + " This is so destructive, it drains 5 AP from them!"
                        if str(target.id) in self.bot.users_ap.keys():
                            new_ap = self.bot.users_ap[str(target.id)] - 5
                            if new_ap < 0:
                                new_ap = 0

                            self.bot.users_ap[str(target.id)] = new_ap

                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "toxinmancer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_toxin)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        await h.add_effect(target, self.bot, "poisoned", amount = 3)
                        hook = "**<:poisoned:791885218558640158>[CRITICAL]<:poisoned:791885218558640158>** + 100 Coolness | " + hook + " This leaves them poisoned!"
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "soulcrusher":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_crusher)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    attacker = ctx.message.author.id

                    if attacker not in self.souls:
                        self.souls[attacker] = []
                    
                    if target.id not in self.souls[attacker] and crit_check == False:
                        self.souls[attacker].append(target.id) # Alter this to make it add them to it, else change crit_check to 100 and do a mega crit.
                    elif target.id in self.souls[attacker]:
                        self.souls[attacker].remove(target.id)
                        crit_check = 100

                    if crit_check == False:
                        await ctx.send(hook)
                    elif crit_check == True:
                        hook = "**✨[SOUL STEAL!]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                    else:
                        hook = "**💀[SOUL CRUSH!]💀** + 400 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 400)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "pacted":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    demon = await h.get_demon(ctx.author.id, self.bot)

                    special_demons = ["zollok", "ilixnith"] # Doing this once here, specifically for demons that have stuff here. This way we avoid doing it multiple times.
                    if demon in special_demons:
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select * from users where id = '{ctx.author.id}';") as info:
                                user = await info.fetchone()
                        level = user[8] - 19

                    crit_check = await h.crit_handler(self.bot, ctx.author.id, target.id)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_pact)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        if demon == "zollok":
                            if ctx.author.id not in self.zollok:
                                self.zollok[ctx.author.id] = 0
                            else:
                                self.zollok[ctx.author.id] = self.zollok[ctx.author.id] + 1
                        await ctx.send(hook)
                    else:
                        if demon == "ilixnith":
                            hook = f"**✨[CRITICAL]✨** + {50*(1+level)} Coolness | " + hook
                            await h.add_coolness(ctx.author.id, 50*(1+level))
                        else:
                            crit_amount = 100
                            if demon == "zollok":
                                if ctx.author.id not in self.zollok:
                                    self.zollok[ctx.author.id] = 0
                                else:
                                    boost = self.zollok[ctx.author.id]*(5*level)
                                    self.zollok[ctx.author.id] = 0
                                crit_amount = 100+boost
                            hook = f"**✨[CRITICAL]✨** + {crit_amount} Coolness | " + hook
                            await h.add_coolness(ctx.author.id, crit_amount)
                        await ctx.send(hook)

                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(apprentice(bot))
