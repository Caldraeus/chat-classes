import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class swordsman(commands.Cog):
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

        self.hooks_w = [
            "usr1 slams their sword into usr2's bdypart, eviscerating it.",
            "usr1 chops usr2's bdypart off.",
            "usr1 throws their sword into usr2's chest, then dropkicks it deeper through them.",
            "usr1 slashes usr2's bdypart off, then stomps on it.",
            "usr1 throws a javelin through usr2's bdypart, then cuts them in half with their sword.",
            "usr1 charges at usr2, shoving their sword through usr2's bdypart and slamming them to the floor.",
            "usr1 shoots a crossbow bolt into usr2's bdypart, then runs up and cuts their leg off, causing usr2 to fall down and get further impaled by the crossbow bolt. A bit overkill, usr1. A bit overkill.",
            "usr1 stands on their knees in front of usr2.\n\n'So, any last words, usr1?'\n\n'Yeah. Just one...'\n\nusr1 then headbuts usr2, knocking them down, then steals usr2's weapon and beats them to death with it. usr1 is breathless, but alive.",
            "usr1 kicks usr2 in the stomach, sending them flying, before slashing them in the bdypart.",
            "usr1 throws a dagger into usr2's knee, crippling them. Then, usr1 runs up and impales usr2's bdypart on their sword.",
            "usr1 knees usr2 in the neck, then throws them across the room into a wall before jumping on them with their sword, killing them.",
            "usr2 is locked in battle with usr1. usr2 keeps throwing attack after attack at usr2, but usr1 avoids them all, then charges into usr2, stabbing them through the bdypart.",
            "usr1 grabs usr2's arm and twists it behind their back, then beats usr2 to death with a club.",
            f"usr1 kicks usr2 into a wall before slashing them in the back {random.randint(2,100)} times. Ouch!"
        ]

        self.hooks_s = [
            "usr1 parries usr2's first attack, then slams their katana into their side.",
            "usr1 is locked in battle with usr2. As they clash, usr1 suddenly realises the pattern of attacking usr2 uses. usr1 smiles.\n\n「これで終いだ!」 yells usr1, as they strike usr2 right between their ribs. Blood sprays, and usr2 collapses, dead.",
            "usr1 charges at usr2, then drops to their knees and slides into usr2 with their sword out, cutting them in half.\n\n「よっしゃー！」 yells usr1, as they raise their katana in victory.",
            "usr1 rides on horseback, approaching usr2. They hop off and slice usr2 down the back as they land. usr2 drops, dead.",
            "usr1 stabs usr2 in the neck, then slices them across their stomach. usr2 collapses, and looks up to usr1.\n\n\"Do it. Kill me. I've lost.\"\n\nusr1 scoffs.\n\n「つまらぬ者を斬る気はない。」\n\nusr1 sheaths their sword, and leaves usr2 behind.",
            "usr1 parries usr2's attack.\n\n「甘い!」 usr1 shouts, before stabbing usr2 straight through the neck. usr2 chokes for a moment, then collapses, life draining from their eyes.",
            "usr1 parries usr2, then flips them over, their blade against usr2's throat.\n\n「死ね。」\n\nusr1 chops usr2's head off, then walks away.",
            "usr1 draws a longbow, and fires an arrow straight into usr2's bdypart.",
            "usr1 slices usr2's leg, causing them to fall to their knees. usr1 hands usr2 a smaller blade. usr2 looks up at usr1, and usr2 nods.\n\nusr2 thrusts the blade into their chest and drops over, dead.\n\n「分をわきまえぬは無礼であろう。」",
            "usr2 charges at usr1, who quickly dodges and raises their sword, cutting usr2's arm off. usr2 attempts to attack usr1, but without an arm fails, passing out. usr1 finishes the job.",
            "usr1 charges at usr2, slicing them straight through the stomach. usr2 freezes, then slowly slides apart. Brutal!",
            "usr1 slams the pommel of their katana into usr2's head, disorienting them. usr1 then slices usr2 across the chest twice, finishing them off by kicking them.",
            "usr1 slashes usr2's bdypart a thousand times, turning it into small pieces.",
            "usr1 parries usr2's attack, then smashes the pommel of their katana into usr2's bdypart, causing them to stumble and fall off a cliff."
        ]

        self.hooks_v = [
            "usr1 grabs usr2's head and knees it, then tosses usr2 aside!",
            "usr1 slams their axe into usr2's bdypart, then forces their axe through them! Brutal!",
            "usr1 tackles usr2 and slams their axe into usr2's skull. Owch.",
            "usr1 kicks usr2 into a wall and swings their axe overhead into usr2's bdypart. Bullseye!",
            "usr1 shoulder slams usr2 then rips their arms off. Holy shit dude, relax.",
            "usr1 throws their axe into usr2's bdypart, then runs up and rips it out, slamming it into their neck, beheading them. Fatality!",
            'usr1 charges usr2, yelling "Ég ríf þig í bita!" before impaking them upon their axe and kneeing them off a cliff. Woah.',
            'usr1 grabs usr2 by the neck and lifts them, whispering "Núna deyrðu" before throwing usr2 through a wall',
            'usr2 tries to attack usr1, but usr1 doesn\'t even flinch. usr1 smiles. "Tidbúin að deyja?" usr1 asks before slicing usr2\'s bdypart off.',
            "usr1 grabs usr2 by the waist and flips them upside down, then slams them into the ground, smushing them."
        ]

        self.hooks_ss = [
            "usr1 blocks usr2's attacks, then slams both swords into usr2's bdypart!!",
            "usr1 throws one sword into usr2's bdypart, then beheads them with the other!",
            "usr1 jumps over usr2, slicing them down the back when they land! Ouch!",
            "usr1 throws dirt into usr2's eyes before slicing them in half!",
            "usr1 kicks usr2 in the groin before throwing a few knives into usr2's bdypart! Damn!",
            "usr1 sweeps usr2's legs with a kick then jams a blade into usr2's bdypart.",
            "usr1 pushes their thumb into usr2's eye before slicing their bdypart off!",
            "usr1 kicks usr2 in the shin before cutting them in half."
        ]

        self.hooks_shg = [
            "usr1 throws a blade into usr2, then kicks it through them! Brutal!",
            "usr1 kicks usr2, then slams a warbanner into their chest!",
            "usr1 rips out usr2's bdypart, then crushes it! Owch!",
            "usr1 swings their blade into usr2's bdypart, then kicks them away!",
            "usr1 slams a warbanner into usr2's bdypart, then yells out a warcry!",
            "usr1 kicks usr2 into a pit, then plants a warbanner!",
            "usr1 slams an elbow into usr2's bdypart, then spears them through a warbanner!",
            "usr1 runs at usr2, yelling 「喰らえ」as they ram usr2 through with a warbanner! Owch!"
        ]

        self.hooks_sb = [
            "usr1 throws their katana into usr2's soul, then rends it from them!",
            "usr1 uses the spirit of fire to set their katana ablaze, then slices cleanly through usr2's bdypart!",
            "usr1 throws the spirit of dust into usr2's eyes, then slams them through a wall before finishing them off with their katana!",
            "usr1 enters the ethereal plane, then jumps out behind usr2, slicing off usr2's bdypart!",
            "usr1 uses the spirit of water to weave around usr2's attacks, then slices usr2's bdypart clean off!",
            "usr1 summons a massive spirit blade, then slices usr2 into a thousand bits! Owie!",
            "usr1 drags usr2 into the spirit realm, cuts their limbs off, then leaves them behind. Brutal stuff, usr1. Brutal stuff."
        ]

        self.hooks_swash = [
            "usr1 swings their cutlass directly into usr2's bdypart! Owch!",
            "usr1 raids usr2's home, stabbing them in the process!",
            "usr1 rams their pirate ship into usr2! How? I don't know!",
            "usr1 throws sand into usr2's eye before slicing them in the bdypart!",
            "usr1 smashes a bottle o' rum over usr2's head, then stabs them in the bdypart. Owch!",
            "usr1 trips usr2 before plunging their cutlass into usr2's bdypart!",
            "usr1's crew beats up usr2! Take that, usr2!",
            "\"Yo ho, yo ho!\" usr1 sings as they stab usr2 in the bdypart. How poetic!"
        ]

        self.hooks_adv = [
            "usr1 drinks a healing potion, then throws the bottle at usr2 before piercing their bdypart with their sword!",
            "usr1 rushes at usr2, parrying their first strike, then slicing them in the bdypart.",
            "usr1 heroically protects their friend before turning and slicing usr2's bdypart off! Nice job!",
            "usr1 kicks usr2 into a wall, then plunges their sword into usr2's bdypart!",
            "usr1 jumps up before slamming their sword into usr2! Owch!",
            "usr1 blocks usr2 with their sword before slashing them in the bdypart!",
            "usr1 runs at usr2 and engages in combat with them! After a minute, usr1 finally emerges victorious!",
            "usr1 equips their Amulet of Health before running at usr2, slicing them in the bdypart!"
        ]

    @commands.command(aliases=['slice'])
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def slic(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "swordsman":
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
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "warrior":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_w)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "samurai":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_s)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**🌸[SENBONZAKURA!]🌸** + 250 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 250)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "viking":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts) 
                    hook = random.choice(self.hooks_v)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        pillage_amount = random.randint(100,300)
                        hook = f"**<:gold:801878856196685854>[PILLAGE!]<:gold:801878856196685854>** + 100 Coolness, + {pillage_amount} Gold | " + hook + f"\n\n*{target.display_name} has been pillaged!*"
                        await h.add_coolness(ctx.author.id, 250)
                        await h.add_gold(ctx.author.id, pillage_amount, self.bot)
                        try:
                            await h.add_gold(target.id, -pillage_amount, self.bot)
                        except TypeError:
                            pass
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "sellsword":
                protected = self.bot.get_cog('sellsword').hired
                keys = list(protected.keys())
                if ctx.author.id in keys:
                    if protected[ctx.author.id] == target.id:
                        await ctx.send("You cannot attack your client!")
                    else:
                        ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                    if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                        crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                        body_part = random.choice(h.body_parts) 
                        hook = random.choice(self.hooks_ss)
                        hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                        hook = hook.replace("bdypart", body_part)
                        hook = hook.replace("usr2", f"**{target.display_name}**")
                        if crit_check == False:
                            await ctx.send(hook)
                        else:
                            hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                            await h.add_coolness(ctx.author.id, 100)
                            await ctx.send(hook)
                else:
                    ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                    if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                        crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                        body_part = random.choice(h.body_parts) 
                        hook = random.choice(self.hooks_ss)
                        hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                        hook = hook.replace("bdypart", body_part)
                        hook = hook.replace("usr2", f"**{target.display_name}**")
                        if crit_check == False:
                            await ctx.send(hook)
                        else:
                            hook = "**✨[CRITICAL]✨** + 100 Coolness | " + hook
                            await h.add_coolness(ctx.author.id, 100)
                            await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "shogun":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_shg)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        members = ctx.guild.members
                        chosen_members = []
                        random.shuffle(members)
                        for member in members:
                            if len(chosen_members) == 3:
                                break
                            else:
                                if str(member.id) in self.bot.registered_users.keys():
                                    chosen_members.append(member)
                        try:
                            hook = "**🌸[CRITICAL STRIKE!]🌸** + 150 Coolness | " + hook + f"\n\nYour battle prowess inspires **{chosen_members[0].display_name}, {chosen_members[1].display_name},** and **{chosen_members[2].display_name}**!"
                        except:
                            hook = "**🌸[CRITICAL STRIKE!]🌸** + 150 Coolness | " + hook + f"\n\nUnfortunately, there's no one around to inspire..."
                        await h.add_coolness(ctx.author.id, 150)
                        await ctx.send(hook)
                        for member in chosen_members:
                            await h.add_effect(member, self.bot, "inspired", amount = 5)
            elif self.bot.users_classes[str(ctx.author.id)] == "master samurai":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_s)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**🌸[SENBONZAKURA!]🌸** + 500 Coolness | " + hook
                        await h.add_coolness(ctx.author.id, 500)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "spirit blade":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_sb)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        hook = "**🌸[CRITICAL!]🌸** + 100 Coolness | " + hook + f"\n\n*{ctx.author.display_name} activates their spirit shroud!*"
                        await h.add_coolness(ctx.author.id, 100)
                        await ctx.send(hook)
                        await h.add_effect(ctx.author, self.bot, "shrouded", amount = 10)
            elif self.bot.users_classes[str(ctx.author.id)] == "swashbuckler":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_swash)
                    hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                    hook = hook.replace("bdypart", body_part)
                    hook = hook.replace("usr2", f"**{target.display_name}**")
                    if crit_check == False:
                        await ctx.send(hook)
                    else:
                        members = ctx.guild.members
                        random.shuffle(members)
                        members.remove(ctx.author) # Don't want people shooting themself
                        
                        try:
                            hook = "**☠️[CRITICAL!]☠️** + 100 Coolness | " + hook + f"\n\nYour ship's cannons fire upon **{members[0].display_name}** and **{members[1].display_name}**, earning you an additional 50 coolness!"
                        except:
                            hook = "**☠️[CRITICAL!]☠️** + 100 Coolness | " + hook + f"\n\nYour ship's cannons don't fire..."
                        
                        await h.add_coolness(ctx.author.id, 150)
                        await ctx.send(hook)
            elif self.bot.users_classes[str(ctx.author.id)] == "adventurer":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_adv)
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
    bot.add_cog(swordsman(bot))
