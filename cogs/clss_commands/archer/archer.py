import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class archer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 shoots an arrow at usr2. A direct hit! That's gotta hurt!",
            "usr1 lets loose an arrow at usr2. Ouch! Right in the bdypart.",
            "usr1 yells 'Look over there!' at usr2. While usr2 isn't looking, they shoot an arrow at usr2, striking their bdypart!",
            "usr1 quickly shoots an arrow at usr2, piercing their bdypart.",
            "Holy shit! usr1 shoots usr2 at mach speed! The arrow completely removes their bdypart!",
            "usr1 stands atop a building in the distance. They lick their finger, and raise it into the air. Speed - 3 knots, southwest. usr1 draws back their bow, adjusts properly and lets an arrow lose... it flies for a moment... and bullseye! It strikes usr2 right in the bdypart! usr2 then collapses off into the riverside.",
            f"usr1 has been hiding in the forest for {random.randint(2,100)} days. Waiting. For what, you ask? usr2. And finally the time has come. usr1 takes aim... and fires! Bullseye! It hits usr2 right in the bdypart! Won't be needing that anymore!",
            "usr1 shoots out usr2's bdypart. Sayonara!",
            "usr1 first shoots out usr2's bdypart before finishing them with a nice clean shot to the head. Ouch!",
            "usr1 stands in front of usr2.\n\n'It's been some time.... usr2.'\n\n'Indeed it has.'\n\n'How are you doing without your bdypart?'\n\n'Fine, no thanks to you. Lets finish this, here and no-'\n\nBefore usr2 can finish, usr1 fires a single arrow into usr2's head. They drop, dead. usr1 sighs. It's finally over.",
            "usr1 shoots usr2 midair! Radical!",
            "usr1 nocks three arrows, then fires them at usr2. As it turns out, it's really innacurate, and only one arrow hits usr2 in the bdypart.",
            "usr2 is just minding their business when BAM! An arrow stright through the bdypart! From the treetops, usr1 smiles. A perfect hit.",
            "usr1 chases after usr2! usr1 sees a shortcut, and takes it, cutting off usr2! usr2 tries to run, but recieves an arrow straight through the bdypart, courtesy of usr1.",
            "usr1 trips, accidentally nocking an arrow, aiming it at usr2, and shooting it. It accidentally pierces usr2's bdypart. Accidentally.",
            "usr1 shoots usr2 with an arrow.",
            "usr1 attempts to shoot usr2 with an arrow, but usr2 disarms them! In a last-ditch effort, usr1 grabs an arrow, then jumps at usr2, stabbing them in the bdypart! Success!",
            "usr1 shoots usr2 in the bdypart.",
            "usr1 beats usr2 to death with their bow. Unconventional, but it works.",
            "usr1 slides on some sick sunglasses, looks the other way, and perfectly shoots an arrow into usr2's bdypart.",
            "usr1 uses a grappling hook to swing past usr2, firing 3 arrows into their bdypart as they do.",
            f"usr1 takes a deep breath... then, with expert speed and precision, fires {random.randint(10,100)} arrows into usr2's bdypart. A bit overkill, sure, but it works!"
        ]

        self.hooks_h = [
            "usr1 shoots their crossbow at usr2, impaling their bdypart.",
            "usr1 quickly fires multiple crossbow bolts into usr2.",
            "usr1 lays a beartrap for usr2, who steps into it like a fool, making an easy shot for usr1.",
            "usr1 throws a bola at usr2, trapping them, then finishes usr2 off with a crossbow bolt to the head.",
            "usr1 throws a glaive at usr2, slicing off their bdypart.",
            "usr1 stalks usr2, following them home. Once usr2 lets their guard down, usr1 fires several crossbow bolts at them, quickly ending them.",
            "usr1 follows usr2's footprints in the mud and finally finds them. usr1 and usr2 engage in a battle, but in the end, usr1 is victorious.",
            "usr1 throws a net over usr2, trapping them. usr1 picks them up and throws the weighted net into a river. Goodbye, usr2!",
            "usr1 shoots a crossbow bolt into usr2's bdypart, causing it to fly out the back of usr2 and impale itself on a wall.",
            "usr1 kicks usr2 into a spike pit trap they had previously set up.",
            "usr1 throws sand into usr2's eyes before kicking them into a pit they had dug earlier.",
            "usr1 easily subdues usr2 before dragging them away into the forest, never to be seen again.",
            "usr1 camouflages themself in the underbrush and waits for usr2 to walk by. When usr2 finally does, usr1 jumps up and stabs usr2, before disappearing once more into the forest.",
            "usr1 tries to sneak up on usr2, but is caught! A battle ensues, and usr2 seems to be winning, when all of a sudden usr2 steps into a net trap set up by usr1. usr1 laughs, then shoots the now hanging usr2 with their crossbow.",
            "usr1 sets a crossbow bolt on fire, then shoots it into usr2's window, setting their house on fire. Brutal!"
        ]
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def arrow(self, ctx, target: discord.Member = None): # Shoots an arrow at someone.
        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "archer":
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
            elif self.bot.users_classes[str(ctx.author.id)] == "hunter":
                ap_works = await h.alter_ap(ctx.message, 1, self.bot)
                if ap_works and await h.can_attack(ctx.author.id, target.id, ctx):
                    crit_check = await h.crit_handler(self.bot, ctx.author, target, ctx.channel)
                    body_part = random.choice(h.body_parts)
                    hook = random.choice(self.hooks_h)
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
    bot.add_cog(archer(bot))
