########################################################
from gevent import monkey as curious_george            # https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
curious_george.patch_all(thread=False, select=False)   #
########################################################
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import helper as h
import aiosqlite
import sys, traceback
from os import listdir
from os.path import isfile, join
from discord.utils import find
import os
from datetime import datetime  
from datetime import timedelta  
from PIL import Image, ImageOps
from jishaku.functools import executor_function
from io import BytesIO
from fancy_text import fancy

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
bot.users_factions = {}
bot.tomorrow = bot.tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
bot.pending_achievements = []
bot.force_reset = False

# custom achievement, and when data wipes, 10k starting gold

if __name__ == '__main__': # Cog loader!
    def load_dir_files(path, dash):
        #print("\n")
        for item in listdir(path):
            if os.path.isdir(path) and item != ".DS_Store" and item != "__pycache__" and not item.endswith(".py") and not item.endswith(".md") and not item.endswith(".json"):
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

    async with aiosqlite.connect('unique.db') as conn: # This code makes sure the bot is enabled, then also makes sure that the bot is in an enabled channel
        # This also preloads some of the db.
        async with conn.execute(f"select * from faction_members;") as dudes:
            members = await dudes.fetchall()
    
    for person in members:
        bot.users_factions[int(person[0])] = int(person[1])


    async with aiosqlite.connect('main.db') as conn: 
        # This also preloads some of the db.
        async with conn.execute(f"select * from servers;") as servers:
            servs = await servers.fetchall()
            for serv in servs:
                bot.servers.append(int(serv[0]))
                banned = serv[1].split('|')
                for item in banned:
                    bot.banned_channels.append(item)
        async with conn.execute(f"select id, class, achievements from users;") as people:
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
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select id from servers where id = '{guild.id}';") as servers:
            server_id = await servers.fetchone()
            if server_id:
                print("Server ({server_id[0]}) is already enabled!")
            else:
                bot.servers.append(guild.id)
                print("Fresh server")
                await conn.execute(f"insert into servers values('{guild.id}', '')")
                await conn.commit()

@bot.event
async def on_guild_remove(guild):
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select id from servers where id = '{guild.id}';") as servers:
            serv = await servers.fetchone()
            if serv:
                print("\n\nBot removed from server, removing from registry\n\n")
                await conn.execute(f"delete from servers where id='{guild.id}'")
                await conn.commit()

@bot.command(aliases=['invite'])
@commands.guild_only()
async def invite_link(ctx):
    await ctx.send("https://discord.com/oauth2/authorize?client_id=713506775424565370&scope=bot&permissions=8")


bot.run('NzEzNTA2Nzc1NDI0NTY1Mzcw.XshXTQ.5XwBZmS-Mf9vNnDSGyi0hWcmZG8') # Official Bot
# bot.run('NzY3MTEyMzU4NjQ0MDIzMzI2.X4tLDg.Mer95w4E9L0HVHupQ7VYu0v3GCs') # Test Branch