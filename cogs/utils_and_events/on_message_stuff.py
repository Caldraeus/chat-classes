from xml.dom.minidom import Attr
import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
import asyncio
from asyncio.exceptions import TimeoutError
import sqlite3
from datetime import datetime
import json
from datetime import datetime  
from datetime import timedelta  
from jishaku.functools import executor_function
from io import BytesIO
from fancy_text import fancy

class utils(commands.Cog): #TODO: Implement faction race commands, and the ability to set faction requirements.
    def __init__(self, bot):
        self.bot = bot

        @bot.check
        def check_command_allow(ctx):
            return (str(ctx.channel.id) not in bot.banned_channels) or (ctx.message.content.lower() == f"{h.prefix}classzone")
    
    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        difference = self.bot.tomorrow - datetime.now().replace(minute=0, second=0, microsecond=0)
        difference = int(difference.total_seconds()/3600) # There has to be a better way of doing this.
        if self.bot.reset_time != difference:
            await self.bot.change_presence(activity=discord.Game(f"Hours Until Rollover: {difference}")) 
            self.bot.reset_time = difference


        if datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) >= self.bot.tomorrow:
            self.bot.tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) 

            # First, we update our homies.
            home = self.bot.get_guild(732632186204979281)
            homies = home.get_role(739141464570986687)
            self.bot.server_boosters = []
            for homie in homies.members:
                self.bot.server_boosters.append(homie.id)

            async with aiosqlite.connect("main.db") as conn: # Second thing we do on a reset is give everyone back their action points
                async with conn.execute(f"select id, class, achievements from users;") as people:
                    usrs = await people.fetchall()
                    for guy in usrs:
                        try:
                            if int(guy[0]) in self.bot.server_boosters and int(guy[0]) != 217288785803608074:
                                self.bot.users_ap[guy[0]] = 40
                            elif int(guy[0]) == 217288785803608074:
                                self.bot.users_ap[guy[0]] = 100
                            else:
                                self.bot.users_ap[guy[0]] = 20

                            self.bot.users_classes[guy[0]] = guy[1]
                        except:
                            pass
            
            # We reset the daily gift counter.
            self.bot.claimed = []

            # We reset our notifcations.
            self.bot.notified = []

            # We reset those who are currently under some sort of protection.
            cog = self.bot.get_cog('sellsword')
            cog.hired = {}

            # We reset artifact usage.
            cog = self.bot.get_cog('artifacts')
            cog.used = []
            
            # We reset any other class-specific things.
            cog = self.bot.get_cog('rogue')
            cog.nomad_homes = {} 
            
            
            print("\n\n\n----------------Daily reset has occurred----------------\n\n\n")
        else:
            pass
        
        context = await self.bot.get_context(message)

        try:
            if context.command == None and str(message.channel.id) not in self.bot.banned_channels:
                await handle_effects(message,self.bot) 
        except:
            pass

        if str(message.author.id) in self.bot.registered_users:
            await h.fetch_random_quest(message,self.bot)
            await asyncio.sleep(.1)
            await h.on_message_quest_handler(message.author, message, self.bot.registered_users,self.bot)
            await asyncio.sleep(.1)
            await h.txt_achievement_handler(message.content.lower(), message.author.id, message,self.bot)
            await asyncio.sleep(.1)
            await h.xp_handler(message.author, message, self.bot)
            
            try:
                for person in self.bot.pending_achievements.keys():
                    if person.id == message.author.id: # Pending achievement
                        mss = await message.channel.send(content=message.author.mention, embed=self.bot.pending_achievements[person])
                        del self.bot.pending_achievements[person]
                        await mss.delete(delay=10)
            except AttributeError:
                pass


async def handle_effects(message, bot): # List of effects in the readme
    speaker = message.author.id
    if speaker in bot.user_status:
        user_effects = bot.user_status[speaker]
        for status in user_effects: # We go through each status affecting the user [NOT ALL APPLY TO ON-MESSAGE EVENTS. THEREFORE, WE NEED IF STATEMENTS]. These are applied in order
            if status[0].lower() == "shatter":
                ### HANDLE STACKS
                if len(message.content.split(" ")) != 1:
                    await h.handle_stacks(bot, status, speaker)
                ### APPLY EFFECT
                mad_content = " "
                if message.content != "":
                    while True:
                        mad_content = " "
                        content = message.content.split(" ")
                        random.shuffle(content)
                        mad_content = mad_content.join(content)
                        if mad_content != message.content or all(x==content[0] for x in content) == True:
                            break

                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await h.webhook_safe_check(message.channel)
                    clone_hook = discord.Webhook.from_url(url, session=session)
                    await clone_hook.send(content=mad_content, username=message.author.display_name, avatar_url=message.author.display_avatar.url)
                break
                
                    
            elif status[0].lower() == "polymorph":
                ### HANDLE STACKS
                await h.handle_stacks(bot, status, speaker)
                ### APPLY EFFECT
                
                urls = [
                    "https://assets-global.website-files.com/5bbd49a137709a4145049ab0/5dd67614e984aa331e6dc8be_Fronde--blog-hero-image_0001_sheep.jpg",
                    "https://thumbs-prod.si-cdn.com/SkuS5xz-Q-kr_-ol6xblY9fsoeA=/fit-in/1600x0/https://public-media.si-cdn.com/filer/d4/f6/d4f6e4bf-8f77-445d-a8f9-e3a74c6a40f0/ewkhdqqwsae0xpo.jpeg",
                    "https://i.guim.co.uk/img/media/22bed68981e92d7a9ff204ed7d7f5776a16468fe/1933_1513_3623_2173/master/3623.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=b7545d644ba9f6bcc673a8bdf6d7db83",
                    "https://images.theconversation.com/files/324133/original/file-20200330-173620-1q1nz5d.jpg?ixlib=rb-1.1.0&rect=0%2C697%2C4635%2C2314&q=45&auto=format&w=1356&h=668&fit=crop",
                    "https://viva.org.uk/wp-content/uploads/2020/05/fun-facts.jpg",
                    "https://spca.bc.ca/wp-content/uploads/lamb-in-grassy-field-825x550.jpg",
                    "https://s7657.pcdn.co/wp-content/uploads/2016/01/Fluffy-sheep-940x480.jpg",
                    "https://www.macmillandictionary.com/external/slideshow/thumb/137411_thumb.jpg",
                    "https://www.abc.net.au/cm/rimage/9673494-3x4-xlarge.jpg?v=3",
                    "https://ichef.bbci.co.uk/news/1024/cpsprodpb/081B/production/_98657020_c0042087-black_faced_sheep-spl.jpg"
                ]
                random.seed(len(message.content))
                sheep_content = ""
                for word in message.content.split(" "):
                    if word[-1] == ".":
                        sheep_content += f"b{random.randint(1,10)*'a'}. "
                    elif word[-1] == "!":
                        sheep_content += f"b{random.randint(1,10)*'a'}! "
                    elif word[-1] == ":":
                        sheep_content += f"b{random.randint(1,10)*'a'}: "
                    elif word[-1] == "?":
                        sheep_content += f"b{random.randint(1,10)*'a'}? "
                    elif word[-1] == ",":
                        sheep_content += f"b{random.randint(1,10)*'a'}, "
                    else:
                        sheep_content += f"b{random.randint(1,10)*'a'} "

                random.seed(message.author.id)
                sheep_name = random.choice(h.sheep_names).title() + " Sheep"
                chosen_url = random.choice(urls)
                print(f"{message.author.mention} : {chosen_url}")
                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await h.webhook_safe_check(message.channel)
                    clone_hook = discord.Webhook.from_url(url, session=session)
                    
                    try:
                        await clone_hook.send(content=sheep_content.capitalize(), username=sheep_name, avatar_url=chosen_url)
                    except:
                        await clone_hook.send(content="Ba"*random.randint(1,20), username=sheep_name, avatar_url=chosen_url)
                break
            elif status[0].lower() == "drunk":
                chance = random.randint(1,5)
                if chance == 5:
                    ### HANDLE STACKS
                    await h.handle_stacks(bot, status, speaker)
                    ### APPLY EFFECT
                    chosen_effect = random.randint(1,4)
                    
                    if chosen_effect == 1:
                        await message.delete()
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(message.channel)
                            clone_hook = discord.Webhook.from_url(url, session=session)
                            await clone_hook.send(content=message.content + " -hic-", username=message.author.display_name, avatar_url=message.author.display_avatar.url)
                        break
                    elif chosen_effect == 2:
                        await message.channel.send(f'*{message.author.display_name} vomits all over the floor.*')
                        break
                    elif chosen_effect == 3:
                        await message.channel.send(f'*{message.author.display_name} stumbles over their own feet, nearly falling over.*')
                        break
                    elif chosen_effect == 3:
                        await message.channel.send(f'*{message.author.display_name} burps.*')
                        break
                    elif chosen_effect == 4:
                        await message.delete()
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(message.channel)
                            clone_hook = discord.Webhook.from_url(url, session=session)
                            await clone_hook.send(content="-hic- " + message.content + " -hic-", username=message.author.display_name, avatar_url=message.author.display_avatar.url)
                    break
            elif status[0].lower() == "wooyeah":
                ### HANDLE STACKS
                await h.handle_stacks(bot, status, speaker)
                ### APPLY EFFECT
                async with aiohttp.ClientSession() as session:
                    url = await h.webhook_safe_check(message.channel)
                    clone_hook = discord.Webhook.from_url(url, session=session)
                    try:
                        await clone_hook.send(content=fancy.bold(message.content), username=message.author.display_name, avatar_url=message.author.display_avatar.url)
                    except:
                        await clone_hook.send(content="wooyeah", username=message.author.display_name, avatar_url=message.author.display_avatar.url)
                    await message.delete()
                    break
            elif status[0].lower() == "burning":
                ### HANDLE STACKS
                await h.handle_stacks(bot, status, speaker)
                ### APPLY EFFECT

                fstring = "🔥 "
                for word in message.content.split():
                    chance = random.randint(1,4)
                    fstring += word + " 🔥 "
                    if chance == 2:
                        fire_words = [
                        "OOH AAAA HOT HOT",
                        "SHIT SHIT HOT AHHHHH",
                        "HOT HOT HOT",
                        "FIRE AHHHH IM BURNING",
                        "AHH AHH AHH",
                        "FIRE FIRE AHHHHH",
                        "AHHH FIRE FIRE FIRE",
                        "HOT FIRE HOT",
                        "A" + "H"*random.randint(5,15),
                        "AH AH AH HELP",
                        "FIRE FIRE FIRE",
                        "OW OW OW OW FIRE",
                        "OWCH OWIE FIRE",
                        "FIRE BURNS HELP",
                        "I AM ON FIRE HELP",
                        "HOT OW HOT",
                        "AH SHIT OWCH",
                        "OWCH OWCH OWCH OWCH FIRE",
                        "SOMEONE GET ME SOME WATER"
                        ]
                        fstring += "**" + random.choice(fire_words) + "** "
                fstring += " 🔥 "
                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await h.webhook_safe_check(message.channel)
                    clone_hook = discord.Webhook.from_url(url, session=session)
                    try:
                        await clone_hook.send(content=fstring, username=message.author.display_name, avatar_url=message.author.display_avatar.url)
                    except:
                        await clone_hook.send(content="**I AM ON FIRE HELP MEEEEEEEEEEEEEEEE**", username=message.author.display_name, avatar_url=message.author.display_avatar.url)

# A setup function the every cog has
def setup(bot):
    bot.add_cog(utils(bot))
