import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

class class_comands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    async def start(self, ctx):
        random.seed(ctx.author.id)
        num = random.randint(1,4)
        clss = h.base_classes[num]
        lead = "a"
        if num == 4:
            lead += "n"
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select id from users where id = '{ctx.message.author.id}';") as person:
                user = await person.fetchone()
                if user:
                    print(f"User {ctx.message.author.id} exists, ignoring command.")
                else:
                    print(f"User {ctx.message.author.id} doesn't exist")
                    ### Add user to database
                    await conn.execute(f"insert into users values('{ctx.message.author.id}', '{clss.lower()}', 0, 0, 'No skills', 0, '0', 'Nothing', 1, 0, False, 0, 8)")
                    async with conn.execute(f"select id, class, achievements, ap from users;") as people:
                        usrs = await people.fetchall()
                        for guy in usrs:
                            user_ach = guy[2].split("|")
                            unlocked = []
                            for stringnum in user_ach: # Just for the if statement. I really hate this and want to fix it eventually.
                                unlocked.append(int(stringnum))
                                
                            self.bot.registered_users[str(guy[0])] = unlocked
                    await conn.commit()
                    ###
                    await ctx.send(f"{ctx.author.mention}, you are {lead} {clss.lower()}. Use `;profile` to view your profile! Use `;classinfo` to see your class-specific commands!")
                    self.bot.users_classes[str(guy[0])] = clss.lower()
                    self.bot.users_ap[str(guy[0])] = 8
        
    @commands.command(aliases=["class"])
    @commands.guild_only()
    async def classinfo(self, ctx, *, clss = None):
        if not clss:
            clss = self.bot.users_classes[str(ctx.author.id)]
        clss = clss.lower()
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select * from classes where class_name = '{clss}';") as cinfo:
                class_info = await cinfo.fetchall()
                class_info = class_info[0]
                profile = discord.Embed(title=f"{clss.title()}'s Info", colour=discord.Colour.from_rgb(128, 128, 128), description=class_info[1])
                profile.add_field(name="Previous Class", value=class_info[3], inline=False)
                abilities = class_info[5].split("|")
                final = ""
                for abil in abilities:
                    final+=abil+"\n"
                profile.add_field(name="Class Abilities", value=final, inline=False)
        
        await ctx.send(embed=profile)
            
    

    """
    @commands.command()
    @commands.guild_only()
    async def stop(self, ctx):
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select id from users where id = '{ctx.message.author.id}';") as person:
                user = await person.fetchone()
                if user:
                    await conn.execute(f"delete from users where id = '{ctx.message.author.id}'")
                    await conn.commit()
                    await ctx.send("Account temporarily disabled. I'll keep your data safe if you ever want to return!")
                else:
                    await ctx.send(f"You already lack an account. You can create one with `{h.prefix}start` if you wish.")
    """
    
    
    @commands.command()
    @commands.guild_only()
    async def test(self, ctx):
        async with aiohttp.ClientSession() as session:
            # testhook = await ctx.channel.create_webhook(name="Test")
            url = await h.webhook_safe_check(ctx.channel)
            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
            await hook.send(content=ctx.message.content, username=ctx.message.author.display_name, avatar_url=ctx.message.author.avatar_url)
    
            


# A setup function the every cog has
def setup(bot):
    bot.add_cog(class_comands(bot))
