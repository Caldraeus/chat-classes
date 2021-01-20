########################################################
from gevent import monkey as curious_george            # https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
curious_george.patch_all(thread=False, select=False)   #
########################################################
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import helper as h
import asyncio
import aiosqlite
import sys, traceback
from os import listdir
from os.path import isfile, join
from discord.utils import find
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import random
import os
from datetime import datetime  
from datetime import timedelta  
from PIL import Image, ImageOps
import requests
from jishaku.functools import executor_function
from io import BytesIO

intents = discord.Intents.all()
bot = discord.Client()
bot = commands.Bot(command_prefix=h.prefix, description="Bot", case_insensitive=True, intents=intents)
bot.remove_command("help")

# Global Variables
bot.banned_channels = []
bot.registered_users = {}
bot.notified = []
bot.servers = []
bot.users_ap = {}
bot.users_classes = {}
bot.user_status = {}
bot.version = '0.2.3'
bot.server_boosters = []
bot.reset_time = 0
bot.claimed = []
bot.tomorrow = bot.tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# custom achievement, and when data wipes, 10k starting gold

if __name__ == '__main__': # Cog loader!
    def load_dir_files(path, dash):
        #print("\n")
        for item in listdir(path):
            if os.path.isdir(path) and item != ".DS_Store" and item != "__pycache__" and not item.endswith(".py") and not item.endswith(".md"):
                new_path = path+f"/{item}"
                load_dir_files(new_path, f"{dash}───")
            elif item.endswith(".py"):
                new_path = path+f"/{item}"
                new_path = new_path.replace(".py", "")
                load_path = new_path.replace("/", ".")
                num = 100
                for letter in str(item + dash):
                    num -= 1
                empty = ""
                if "special_classes" in path:
                    num += 3
                for i in range(num): # Makes things look nicer in the console... lol
                    empty += " "
                try:
                    if "special_classes" in path:
                        dash = '├───────'
                    print(f"{dash} Loading {item}...", end = " ")# print(f"[{path}] : Loading {item}...", end = " ")
                    bot.load_extension(load_path)
                    print(f"{empty}[SUCCESS]")
                except (discord.ClientException, ModuleNotFoundError):
                    print(f"\n{empty}[FAILURE]")
                    print(f'Failed to load extension {item}.\n')
                    traceback.print_exc()

    load_dir_files('cogs' ,"├─")
    bot.load_extension('jishaku') # For sync to async

@bot.event
async def on_ready():
    home = bot.get_guild(732632186204979281)
    homies = home.get_role(739141464570986687)
    for homie in homies.members:
        bot.server_boosters.append(homie.id)

    async with aiosqlite.connect('main.db') as conn: # This code makes sure the bot is enabled, then also makes sure that the bot is in an enabled channel
        # This also preloads some of the db.
        async with conn.execute(f"select * from servers;") as servers:
            servs = await servers.fetchall()
            for serv in servs:
                bot.servers.append(int(serv[0]))
                banned = serv[1].split('|')
                for item in banned:
                    bot.banned_channels.append(item)
        async with conn.execute(f"select id, class, achievements, ap from users;") as people:
            usrs = await people.fetchall()
            for guy in usrs:
                user_ach = guy[2].split("|")
                unlocked = []
                for stringnum in user_ach: # Just for the if statement. I really hate this and want to fix it eventually.
                    unlocked.append(int(stringnum))
                    
                bot.registered_users[guy[0]] = unlocked
                
                if int(guy[0]) in bot.server_boosters and int(guy[0]) != 217288785803608074:
                    bot.users_ap[guy[0]] = 40
                elif int(guy[0]) == 217288785803608074:
                    bot.users_ap[guy[0]] = 5000
                else:
                    bot.users_ap[guy[0]] = 20 

                bot.users_classes[guy[0]] = guy[1]
                bot.user_status[int(guy[0])] = []

    print(f'\n\nLogged in.\nThanks.')

@bot.event
async def on_guild_channel_delete(channel):
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select * from webhooks where channel_id = '{channel.id}';") as chan:
            hook = await chan.fetchone()
            if hook:
                await conn.execute(f"delete from webhooks where channel_id = '{channel.id}'")
                await conn.commit()

@bot.event
async def on_guild_join(guild): # Warn the server owner that the bot does... a lot.
    for channel in guild.text_channels:
        if "bots" in channel.name or "general" in channel.name or "chat" in channel.name or "lobby" in channel.name or "main" in channel.name: # This is gross. Don't do this.
            print(f"Keyword found in {channel.name}.")
            chan = channel
            break
    if chan:
        if chan.permissions_for(guild.me).send_messages:
            await chan.send(f'Greetings, members of {guild.name}! Before this bot is active, the owner must understand that this bot messes with chat quite a bit. This includes sending messages, deleting messages, and creating (temporary!) channels. This bot will not destroy your server, I promise. I would only recommend this bot for small servers with friends/etc. For more information on managing this bot and what it does, use `;help` and read on how to disable the bot in specific channels.\n\nNow that that is all said and done, I will need the server owner ({guild.owner.mention}) to say `{h.prefix}enablecc`\n\nAdditionally, this bot makes use of nickname permissions, and it needs the highest role in a guild to operate. If you do not feel comfortable doing this, I understand, but you should recognise that this bot will have less functionality.\n\n__**PLEASE GIVE THIS BOT THE HIGHEST ROLE IN THE SERVER FOR IT TO WORK PROPERLY!**__\n\nThat is all!')

@bot.event
async def on_guild_remove(guild):
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select id from servers where id = '{guild.id}';") as servers:
            serv = await servers.fetchone()
            if serv:
                print("\n\nBot removed from server, removing from registry\n\n")
                await conn.execute(f"delete from servers where id='{guild.id}'")
                await conn.commit()

@bot.event
async def on_message(message):
    difference = bot.tomorrow - datetime.now().replace(minute=0, second=0, microsecond=0)
    difference = int(difference.total_seconds()/3600) # There has to be a better way of doing this.
    if bot.reset_time != difference:
        await bot.change_presence(activity=discord.Game(f"Hours Until Rollover: {difference}")) 
        bot.reset_time = difference


    if datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) >= bot.tomorrow:
        bot.tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) 

        # First, we update our homies.
        home = bot.get_guild(732632186204979281)
        homies = home.get_role(739141464570986687)
        bot.server_boosters = []
        for homie in homies.members:
            bot.server_boosters.append(homie.id)

        async with aiosqlite.connect("main.db") as conn: # Second thing we do on a reset is give everyone back their action points
            async with conn.execute(f"select id, class, achievements, ap from users;") as people:
                usrs = await people.fetchall()
                for guy in usrs:
                    try:
                        if int(guy[0]) in bot.server_boosters and int(guy[0]) != 217288785803608074:
                            bot.users_ap[guy[0]] = 40
                        elif int(guy[0]) == 217288785803608074:
                            bot.users_ap[guy[0]] = 100
                        else:
                            bot.users_ap[guy[0]] = 20

                        bot.users_classes[guy[0]] = guy[1]
                    except:
                        pass
        
        # We reset the daily gift counter.
        bot.claimed = []

        # We reset artifact usage.
        cog = bot.get_cog('artifacts')
        cog.used = []
        
        
        print("\n\n\n----------------Daily reset has occurred----------------\n\n\n")
    else:
        pass
    
    ctx = await bot.get_context(message)
    if not message.author.bot:
        if (str(message.channel.id) not in bot.banned_channels) or message.content.lower() == f"{h.prefix}classzone" or message.author.id == 67217288785803608074: # Put in-chat things here, as this is where it makes sure the channel is enabled.
            if message.guild.id in bot.servers or message.content.lower() == f"{h.prefix}enablecc":
                await bot.process_commands(message) # Run commands.
            elif message.content[0] == ";":
                await message.channel.send("⚠️ | Hey! Seems like you're trying to run a command. Sadly, the bot hasn't been activated for this server yet, or I'm still loading! If I'm not enabled, have the server owner say `;enablecc`")
        # Here is how we handle on-message effects that can be caused by some classes.
            try:
                if ctx.command == None:
                    await handle_effects(message, bot)
            except:
                pass

        if str(message.author.id) in bot.registered_users:
            await h.fetch_random_quest(message, bot)
            await asyncio.sleep(.1)
            await h.on_message_quest_handler(message.author, message, bot.registered_users, bot)
            await asyncio.sleep(.1)
            await h.txt_achievement_handler(message.content.lower(), message.author.id, message, bot)
            await asyncio.sleep(.1)
            await h.xp_handler(message, bot)

@bot.command(aliases=['invite'])
@commands.guild_only()
async def invite_link(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=713506775424565370&scope=bot&permissions=8")

"""
@bot.command()
@commands.guild_only()
async def test(ctx):
    origin = await h.find_origin("pacted")
    await ctx.send(f"You started as: {origin}")
"""

###### The following below is implemented here rather than in helper due to the nature of it's blocking commands that I need to use jishaku's stuff for 

@executor_function # makes sync int
def shatter_image(url):
    with Image.open(requests.get(url, stream=True).raw) as im:
        im = ImageOps.mirror(im)
        buff = BytesIO()
        im.save(buff, 'png')
    buff.seek(0)
    return buff


async def handle_effects(message, bot): # List of effects in the readme
    speaker = message.author.id
    if speaker in bot.user_status:
        user_effects = bot.user_status[speaker]
        for status in user_effects: # We go through each status affecting the user [NOT ALL APPLY TO ON-MESSAGE EVENTS. THEREFORE, WE NEED IF STATEMENTS]. These are applied in order
            if status[0].lower() == "shatter":
                ### HANDLE STACKS
                if len(message.content.split(" ")) != 1:
                    remaining_stacks = status[1]-1
                    if remaining_stacks <= 0:
                        bot.user_status[speaker].remove(status)
                    else:
                        status[1] -= 1
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
                if message.attachments != []:
                    if len(message.attachments) == 1:
                        buff = await shatter_image(url=message.attachments[0].url)
                        buff = discord.File(fp=buff, filename='fucked_image.png')
                    else:
                        buff = None
                else:
                    buff = None

                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await h.webhook_safe_check(message.channel)
                    clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    await clone_hook.send(content=mad_content, username=message.author.display_name, avatar_url=message.author.avatar_url, file=buff)
                    
            elif status[0].lower() == "polymorph":
                ### HANDLE STACKS
                remaining_stacks = status[1]-1
                if remaining_stacks <= 0:
                    bot.user_status[speaker].remove(status)
                else:
                    status[1] -= 1
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
                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await h.webhook_safe_check(message.channel)
                    clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    
                    try:
                        await clone_hook.send(content=sheep_content.capitalize(), username=sheep_name, avatar_url=chosen_url)
                    except:
                        await clone_hook.send(content="Ba"*random.randint(1,20), username=sheep_name, avatar_url=chosen_url)
            elif status[0].lower() == "drunk":
                chance = random.randint(1,5)
                if chance == 5:
                    ### HANDLE STACKS
                    remaining_stacks = status[1]-1
                    if remaining_stacks <= 0:
                        bot.user_status[speaker].remove(status)
                    else:
                        status[1] -= 1
                    ### APPLY EFFECT
                    chosen_effect = random.randint(1,4)
                    
                    if chosen_effect == 1:
                        await message.delete()
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(message.channel)
                            clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await clone_hook.send(content=message.content + " -hic-", username=message.author.display_name, avatar_url=message.author.avatar_url)
                    elif chosen_effect == 2:
                        await message.channel.send(f'*{message.author.display_name} vomits all over the floor.*')
                    elif chosen_effect == 3:
                        await message.channel.send(f'*{message.author.display_name} stumbles over their own feet, nearly falling over.*')
                    elif chosen_effect == 3:
                        await message.channel.send(f'*{message.author.display_name} burps.*')
                    elif chosen_effect == 4:
                        await message.delete()
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(message.channel)
                            clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await clone_hook.send(content="-hic- " + message.content + " -hic-", username=message.author.display_name, avatar_url=message.author.avatar_url)
            elif status[0].lower() == "burning":
                ### HANDLE STACKS
                remaining_stacks = status[1]-1
                if remaining_stacks <= 0:
                    bot.user_status[speaker].remove(status)
                else:
                    status[1] -= 1
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
                    clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    try:
                        await clone_hook.send(content=fstring, username=message.author.display_name, avatar_url=message.author.avatar_url)
                    except:
                        await clone_hook.send(content="**I AM ON FIRE HELP MEEEEEEEEEEEEEEEE**", username=message.author.display_name, avatar_url=message.author.avatar_url)

####

bot.run('NzEzNTA2Nzc1NDI0NTY1Mzcw.XshXTQ.5XwBZmS-Mf9vNnDSGyi0hWcmZG8') # Official Bot
# bot.run('NzY3MTEyMzU4NjQ0MDIzMzI2.X4tLDg.Mer95w4E9L0HVHupQ7VYu0v3GCs') 