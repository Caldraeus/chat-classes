import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class scholar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hooks = [
            "usr1 studies magic."
        ]
        self.subjects = [
            "magic",
            "abjuration magic",
            "conjuration magic",
            "calling magic",
            "creation",
            "healing",
            "summoning",
            "teleportation",
            "divination magic",
            "scrying magic",
            "enchantment magic",
            "charming magic",
            "compulsion magic",
            "evocation magic",
            "figment magic",
            "illusions",
            "phantasms",
            "shadows",
            "transmutation",
            "polymorphing",
            "the universe",
            "dogs",
            "cats",
            "alchemy",
            "nature",
            "thaumaturgy",
            "transformation",
            "fighting"
        ]
    pass

    @commands.command()
    @commands.guild_only()
    async def study(self, ctx): 
        if self.bot.users_classes[str(ctx.author.id)] == "scholar":
            ap_works = await h.alter_ap(ctx.message, 5, self.bot)
            if ap_works:
                crit_check = random.randint(1,20)
                body_part = random.choice(h.body_parts)
                hook = random.choice(self.hooks)
                hook = hook.replace("usr1", f"**{ctx.author.display_name}**")
                hook = hook.replace("magic", random.choice(self.subjects))

                xp_gained = random.randint(1, 100)

                if crit_check != 20:
                    await ctx.send(f"+{xp_gained} XP | {hook}")

                    async with aiosqlite.connect('main.db') as conn:
                        async with conn.execute(f"select exp from users where id = '{ctx.author.id}'") as exp:
                            old_exp = await exp.fetchone()
                            new_exp = old_exp[0] + xp_gained
                            await conn.execute(f"update users set exp = {new_exp} where id = '{ctx.author.id}';")
                            await conn.commit() 

                else:
                    hook = "**💡[EPIPHANY]💡** + 300 XP | " + hook
                    await ctx.send(hook)

                    async with aiosqlite.connect('main.db') as conn:
                        async with conn.execute(f"select exp from users where id = '{ctx.author.id}'") as exp:
                            old_exp = await exp.fetchone()
                            new_exp = old_exp[0] + 300
                            await conn.execute(f"update users set exp = {new_exp} where id = '{ctx.author.id}';")
                            await conn.commit() 
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(scholar(bot))
