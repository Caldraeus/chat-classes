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
bot.version = '0.2.1'
bot.server_boosters = []
bot.reset_time = 0
bot.claimed = []
bot.tomorrow = bot.tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)



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
                elif int(guy[0]) in bot.server_boosters and int(guy[0]) == 217288785803608074:
                    bot.users_ap[guy[0]] = 100
                else:
                    bot.users_ap[guy[0]] = 20 

                bot.users_classes[guy[0]] = guy[1]

    print(f'\n\nLogged in.')
    update = None
    print("Thanks.")


    if update:
        channel = bot.get_channel(734108098129821757)
        embed = discord.Embed(title=f"⭐ New Update! ⭐", colour=discord.Colour.from_rgb(21,244,238), description=update)
        mss = await channel.send(content="╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲", embed=embed)
        await mss.publish()

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
                    if int(guy[0]) in bot.server_boosters and int(guy[0]) != 217288785803608074:
                        bot.users_ap[guy[0]] = 40
                    elif int(guy[0]) in bot.server_boosters and int(guy[0]) == 217288785803608074:
                        bot.users_ap[guy[0]] = 100
                    else:
                        bot.users_ap[guy[0]] = 20

                    bot.users_classes[guy[0]] = guy[1]
        
        # We reset the daily gift counter.
        bot.claimed = []
        
        
        print("\n\n\n----------------Daily reset has occurred----------------\n\n\n")
    else:
        pass
        
    if not message.author.bot:
        if (str(message.channel.id) not in bot.banned_channels) or message.content.lower() == f"{h.prefix}classzone" or message.author.id == 67217288785803608074: # Put in-chat things here, as this is where it makes sure the channel is enabled.
            if message.guild.id in bot.servers or message.content.lower() == f"{h.prefix}enablecc":
                await bot.process_commands(message) # Run commands.
            elif message.content[0] == ";":
                await message.channel.send("⚠️ | Hey! Seems like you're trying to run a command. Sadly, the bot hasn't been activated for this server yet, or I'm still loading! If I'm not enabled, have the server owner say `;enablecc`")
        if str(message.author.id) in bot.registered_users:
            await h.fetch_random_quest(message, bot)
            await asyncio.sleep(.1)
            await h.on_message_quest_handler(message.author, message, bot.registered_users)
            await asyncio.sleep(.1)
            await h.txt_achievement_handler(message.content.lower(), message.author.id, message, bot)
            await asyncio.sleep(.1)
            await h.xp_handler(message, bot)

@bot.command(aliases=['invite'])
@commands.guild_only()
async def invite_link(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=713506775424565370&scope=bot&permissions=8")



bot.run('NzEzNTA2Nzc1NDI0NTY1Mzcw.XshXTQ.5XwBZmS-Mf9vNnDSGyi0hWcmZG8') # Official Bot
# bot.run('NzY3MTEyMzU4NjQ0MDIzMzI2.X4tLDg.Mer95w4E9L0HVHupQ7VYu0v3GCs') # Test Branch