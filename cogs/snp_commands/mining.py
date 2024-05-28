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

class mining(commands.Cog): #TODO: Implement faction race commands, and the ability to set faction requirements.
    def __init__(self, bot):
        self.bot = bot
        self.smelting = {}

        self.mine_hooks = [
            "You dig up amount ore while mining!",
            "You spend many hours in the mine, and eventually find amount ore!",
            "After a few hours, you return from the mine with amount ore!",
            "Nice! You found amount ore while mining!",
            "You mine amount ore.",
            "Your mining expedition rewards you with amount ore."
        ]

        self.smelting = []

        self.smelting_rates = {
            802597628759375913 : 75,
            802599362885582879 : 60,
            802599364013850698 : 50,
            802601524257095700 : 40,
            802601869503365151 : 30,
            802602269324345346 : 20,
            802602115180134431 : 5,
        }

        self.smelting_cost = {
            802597628759375913 : 50,
            802599362885582879 : 60,
            802599364013850698 : 50,
            802601524257095700 : 40,
            802601869503365151 : 30,
            802602269324345346 : 20,
            802602115180134431 : 10,
        }

        self.materials = {
            "stone" : None,
            "coal" : None,
            "iron" : "Iron Ingot",
            "silver" : "Silver Ingot",
            "bronze" : "Bronze Ingot",
            "gold" : "Gold Ingot",
            "sulfur" : None,
            "arsenic" : None,
            "faux gold" : "Faux Gold Ingot",
            "amber" : None,
            "cobalt" : "Cobalt Ingot",
            "emerald" : "Refined Emerald",
            "iridium" : "Refined Iridium",
            "experium" : "Experience",
            "black diamond" : None,
            "lightstone" : "Bright Ingot",
            "thunderstone" : "Thunder Ingot",
            "deepstone" : "Deep Ingot",
            "starbit" : "Astral Ingot",
            "blood diamond" : None,
            "dragonstone" : "Draconic Ingot",
            "moonstone" : "Lunar Ingot",
            "eldritch copper" : "Lovecraftian Ingot",
            "naruulite" : "Vita Ingot",
            "unobtanium" : "Unobtanium Ingot",
            "jazzium" : "Jazzed Up Ingot",
            "fearite" : "Ethereal Ingot",
            "astral gem" : None,
            "mythril" : "Mythril Ingot",
            "obsidian" : "Packed Obsidian"
        }

        
    pass

    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)

    def is_in_cat():
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.category_id == 802594173663314004
        return commands.check(predicate)

    def is_in_chan(chan):
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.id == chan
        return commands.check(predicate)

    pass # EOF

    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    async def skills(self, ctx, target: discord.Member = None):
        if target == None:
            target = ctx.author
        async with aiosqlite.connect('snp.db') as conn:
            async with conn.execute(f"SELECT * FROM skill_levels WHERE uid = {target.id};") as count:
                current_amount = await count.fetchall()
        if current_amount != []:
            skill_stats = current_amount[0]
            profile = discord.Embed(title=f"{target.display_name}'s Skills", colour=discord.Colour.from_rgb(255,255,255), description="")
            profile.set_thumbnail(url=target.display_avatar.url)

            profile.add_field(name=f"Mining Level : {skill_stats[1]}", value=f"{skill_stats[3]} / {h.max_xp_skills(int(skill_stats[1]))} XP")
            profile.add_field(name=f"Foraging Level : {skill_stats[2]}", value=f"{skill_stats[4]} / {h.max_xp_skills(int(skill_stats[2]))} XP")

            await ctx.send(embed=profile)

        else:
            await ctx.send("User hasn't started using any skills!")
        

        
    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    @is_in_chan(803111236052320327)
    async def smelt(self, ctx, amount: int, *, material):
        if amount <= 0:
            await ctx.send("Nice try bucko. Use a positive amount next time.")
        else:
            material = material.title()
            if ctx.author.id in self.smelting:
                await ctx.send("You already have an ongoing smelting task! I'll mention you when it's all done!")
            else:
                member = ctx.guild.get_member(ctx.author.id)
                
                for role in member.roles:
                    if role.id in self.smelting_rates.keys():
                        smelting_time = self.smelting_rates[role.id]

                for role in member.roles:
                    if role.id in self.smelting_rates.keys():
                        smelting_cost = self.smelting_rates[role.id]
                try:
                    if material.lower() in self.materials.keys():
                        new_material = self.materials[material.lower()]
                        if new_material != None:
                            await update_materials(ctx.author.id, ["coal", material], [-smelting_cost, -amount], ctx)

                            self.smelting.append(ctx.author.id)

                            await ctx.send(f"<:smelt:803481215788384258> | Forges ignited! Your task will be done in {smelting_time} minutes!")
                            await asyncio.sleep(smelting_time*60) # smelting_time*60
                            await ctx.send(f"{ctx.author.mention} : Your smelting task has finished! (**{material}** ⮕ **{new_material}**)")
                            self.smelting.remove(ctx.author.id)
                            while ctx.author.id in self.smelting:
                                self.smelting.remove(ctx.author.id)
                            if material == "Experium":
                                await h.xp_handler(ctx.author, ctx.message, self.bot, boost = amount)
                            else:
                                await update_materials(ctx.author.id, new_material, amount, ctx)
                        else:
                            await ctx.send("That material is unable to be further smelted!")
                    else:
                        await ctx.send("That material doesn't exist, or can't be smelted! Did you make a typo?")
                except MaterialError as err:
                    await ctx.send(f"You don't have enough of either coal or that material for this! You need at least **{smelting_cost}** coal and at least **{amount}** {material} to smelt!")
                

    @commands.command(aliases=["mats"])
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    @is_in_guild(732632186204979281)
    async def materials(self, ctx):
        async with aiosqlite.connect('snp.db') as conn:
            async with conn.execute(f"SELECT item_name, amount FROM materials WHERE uid = {ctx.author.id} order by item_name;") as count:
                current_amount = await count.fetchall()

        lists = 1
        final_list = ""
        final_list_2 = ""
        for item in current_amount:
            if len(final_list) < 2000:
                if int(item[1]) != 0:
                    final_list += f"**{item[0]}:** {item[1]}\n"
            elif len(final_list_2) < 2000:
                lists = 2
                if int(item[1]) != 0:
                    final_list_2 += f"**{item[0]}:** {item[1]}\n"
        
        if lists == 1:
            profile = discord.Embed(title=f"{ctx.author.display_name}'s Materials", colour=discord.Colour.from_rgb(95,71,47), description=final_list)
            profile.set_thumbnail(url=ctx.author.display_avatar.url)

            await ctx.send(embed=profile)
        elif lists == 2:
            profile = discord.Embed(title=f"{ctx.author.display_name}'s Materials (Page 1)", colour=discord.Colour.from_rgb(95,71,47), description=final_list)
            profile.set_thumbnail(url=ctx.author.display_avatar.url)

            await ctx.send(embed=profile)

            profile = discord.Embed(title=f"{ctx.author.display_name}'s Materials (Page 2)", colour=discord.Colour.from_rgb(95,71,47), description=final_list_2)

            await ctx.send(embed=profile)


    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    @is_in_guild(732632186204979281)
    @is_in_cat()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def mine(self, ctx):
        ## Ore rarities. I would do this in self, but I want the amount to change every time.
        ore_rarity_beginner = RelativeWeightedChoice((
            (2000, ["Stone", random.randint(3,30)]),
            (2000, ["Coal", random.randint(60,300)]),
            (1950, ["Iron", random.randint(5,10)]),
            (1950, ["Silver", random.randint(5,10)]),
            (1900, ["Bronze", random.randint(5, 10)]),
            (700, ["Gold", random.randint(2,10)]),
            (700, ["Sulfur", random.randint(2,5)]),
            (700, ["Arsenic", random.randint(2,5)]),
            (700, ["Faux Gold", random.randint(2,8)]),
            (500, ["Amber", random.randint(1,3)]),
            (500, ["Cobalt", random.randint(1,3)]),
            (500, ["Emerald", random.randint(1,3)]),
            (100, ["Experium", random.randint(100,500)]),
            (100, ["Reactive Prism", 1])
        ))

        ore_rarity_novice = RelativeWeightedChoice((
            (1600, ["Stone", random.randint(3,30)]),
            (1600, ["Coal", random.randint(60,300)]),
            (1600, ["Iron", random.randint(5,10)]),
            (1600, ["Silver", random.randint(5,10)]),
            (1600, ["Bronze", random.randint(5, 10)]),
            (900, ["Gold", random.randint(2,20)]),
            (900, ["Sulfur", random.randint(2,15)]),
            (900, ["Arsenic", random.randint(2,15)]),
            (900, ["Faux Gold", random.randint(2,18)]),
            (600, ["Amber", random.randint(1,13)]),
            (600, ["Cobalt", random.randint(1,13)]),
            (600, ["Emerald", random.randint(1,13)]),
            (600, ["Experium", random.randint(100,500)]),
            (175, ["Reactive Prism", random.randint(1,3)]),
            (175, ["Diamond", random.randint(1,3)]),
            (175, ["Amethyst", random.randint(1,3)]),
            (175, ["Ruby", random.randint(1,3)]),
            (175, ["Mythril", random.randint(1,3)]),
            (175, ["Magma", random.randint(1,3)]),
            (175, ["Obsidian", random.randint(1,3)])
        ))

        ore_rarity_advanced = RelativeWeightedChoice((
            (1400, ["Stone", random.randint(3,30)]),
            (1400, ["Coal", random.randint(60,500)]),
            (1400, ["Iron", random.randint(5,10)]),
            (1400, ["Silver", random.randint(5,10)]),
            (1400, ["Bronze", random.randint(5, 10)]),
            (1000, ["Gold", random.randint(2,20)]),
            (1000, ["Sulfur", random.randint(2,15)]),
            (1000, ["Arsenic", random.randint(2,15)]),
            (1000, ["Faux Gold", random.randint(2,18)]),
            (900, ["Amber", random.randint(1,13)]),
            (900, ["Cobalt", random.randint(1,13)]),
            (900, ["Emerald", random.randint(1,13)]),
            (900, ["Experium", random.randint(100,500)]),
            (500, ["Reactive Prism", random.randint(1,13)]),
            (500, ["Diamond", random.randint(1,13)]),
            (500, ["Amethyst", random.randint(1,13)]),
            (500, ["Ruby", random.randint(1,13)]),
            (500, ["Mythril", random.randint(1,13)]),
            (500, ["Magma", random.randint(1,13)]),
            (500, ["Obsidian", random.randint(1,13)]),
            (200, ["Black Diamond", random.randint(1,2)]),
            (200, ["Lightstone", random.randint(1,2)]),
            (200, ["Thunderstone", random.randint(1,2)]),
            (200, ["Plutonium", random.randint(1,2)]),
            (200, ["Deepstone", random.randint(1,2)]),
        ))

        ore_rarity_expert = RelativeWeightedChoice((
            (900, ["Gold", random.randint(2,20)]),
            (900, ["Sulfur", random.randint(2,15)]),
            (900, ["Arsenic", random.randint(2,15)]),
            (900, ["Faux Gold", random.randint(2,18)]),
            (1000, ["Amber", random.randint(10,23)]),
            (1000, ["Cobalt", random.randint(10,23)]),
            (1000, ["Emerald", random.randint(10,23)]),
            (1000, ["Experium", random.randint(100,500)]),
            (900, ["Reactive Prism", random.randint(5,13)]),
            (900, ["Diamond", random.randint(5,13)]),
            (900, ["Amethyst", random.randint(5,13)]),
            (900, ["Ruby", random.randint(5,13)]),
            (900, ["Mythril", random.randint(5,13)]),
            (900, ["Magma", random.randint(5,13)]),
            (900, ["Obsidian", random.randint(5,13)]),
            (450, ["Black Diamond", random.randint(5,12)]),
            (450, ["Lightstone", random.randint(5,12)]),
            (450, ["Thunderstone", random.randint(5,12)]),
            (450, ["Plutonium", random.randint(5,12)]),
            (450, ["Deepstone", random.randint(5,12)]),
            (450, ["Starbit", random.randint(5,12)])
        ))

        ore_rarity_master = RelativeWeightedChoice((
            (1000, ["Amber", random.randint(10,23)]),
            (1000, ["Cobalt", random.randint(10,23)]),
            (1000, ["Emerald", random.randint(10,23)]),
            (1000, ["Experium", random.randint(100,500)]),
            (900, ["Reactive Prism", random.randint(5,13)]),
            (900, ["Diamond", random.randint(5,13)]),
            (900, ["Amethyst", random.randint(5,13)]),
            (900, ["Ruby", random.randint(5,13)]),
            (900, ["Mythril", random.randint(5,13)]),
            (900, ["Magma", random.randint(5,13)]),
            (900, ["Obsidian", random.randint(5,13)]),
            (450, ["Black Diamond", random.randint(5,12)]),
            (450, ["Lightstone", random.randint(5,12)]),
            (450, ["Thunderstone", random.randint(5,12)]),
            (450, ["Plutonium", random.randint(5,12)]),
            (450, ["Deepstone", random.randint(5,12)]),
            (450, ["Starbit", random.randint(5,12)]),
            (100, ["Dragonstone", 1]),
            (100, ["Moonstone", 1]),
            (100, ["Eldritch Copper", 1]),
            (100, ["Naruulite", 1]),
            (100, ["Iridium", random.randint(1,4)]),
            (5, ["Unobtanium", 1])
            
        ))

        ore_rarity_legendary = RelativeWeightedChoice((
            (1000, ["Reactive Prism", random.randint(5,13)]),
            (1000, ["Diamond", random.randint(5,13)]),
            (1000, ["Amethyst", random.randint(5,13)]),
            (1000, ["Ruby", random.randint(5,13)]),
            (1000, ["Mythril", random.randint(5,13)]),
            (1000, ["Magma", random.randint(5,13)]),
            (1000, ["Obsidian", random.randint(5,13)]),
            (500, ["Black Diamond", random.randint(5,12)]),
            (500, ["Lightstone", random.randint(5,12)]),
            (500, ["Thunderstone", random.randint(5,12)]),
            (500, ["Plutonium", random.randint(5,12)]),
            (500, ["Deepstone", random.randint(5,12)]),
            (500, ["Starbit", random.randint(5,12)]),
            (250, ["Dragonstone", random.randint(1,10)]),
            (250, ["Moonstone", random.randint(1,10)]),
            (250, ["Eldritch Copper", random.randint(1,10)]),
            (250, ["Naruulite", random.randint(1,10)]),
            (250, ["Iridium", random.randint(1,14)]),
            (100, ["Unobtanium", random.randint(1,2)]),
            (100, ["Raw Void", random.randint(1,2)]),
            (100, ["Unobtanium", random.randint(1,20)]),
            (100, ["Jazzium", random.randint(1,2)]),
            (100, ["Fearite", random.randint(1,2)]),
            (100, ["Astral Gem", random.randint(1,2)])  
        ))

        ore_rarity_gmaster = RelativeWeightedChoice((
            (1500, ["Black Diamond", random.randint(5,12)]),
            (1500, ["Lightstone", random.randint(5,12)]),
            (1500, ["Thunderstone", random.randint(5,12)]),
            (1500, ["Plutonium", random.randint(5,12)]),
            (1500, ["Deepstone", random.randint(5,12)]),
            (1500, ["Starbit", random.randint(5,12)]),
            (1250, ["Dragonstone", random.randint(1,10)]),
            (1250, ["Moonstone", random.randint(1,10)]),
            (1250, ["Eldritch Copper", random.randint(1,10)]),
            (1250, ["Naruulite", random.randint(1,10)]),
            (1250, ["Iridium", random.randint(1,14)]),
            (500, ["Unobtanium", random.randint(1,12)]),
            (500, ["Raw Void", random.randint(1,12)]),
            (500, ["Unobtanium", random.randint(1,12)]),
            (500, ["Jazzium", random.randint(1,12)]),
            (500, ["Fearite", random.randint(1,12)]),
            (500, ["Astral Gem", random.randint(1,12)])  
        ))

        ##
        member = ctx.guild.get_member(ctx.author.id)
        if str(ctx.author.id) in self.bot.users_classes.keys():
            ap_works = await h.alter_ap(ctx.message, 2, self.bot)
            if ap_works:
                if ctx.channel.id == 802593427484442644:
                    ore = ore_rarity_beginner()
                elif ctx.channel.id == 802599306116071454:
                    ore = ore_rarity_novice()
                elif ctx.channel.id == 802600195254517771:
                    ore = ore_rarity_advanced()
                elif ctx.channel.id == 802602442680041512:
                    ore = ore_rarity_expert()
                elif ctx.channel.id == 802603025511874560:
                    ore = ore_rarity_master()
                elif ctx.channel.id == 802603276234784838:
                    ore = ore_rarity_legendary()
                elif ctx.channel.id == 802603445172830288:
                    ore = ore_rarity_gmaster()
                
                amount = ore[1]
                ore = ore[0]
                # max_xp_skills
                xp_gained = random.randint(5,20)

                hook = random.choice(self.mine_hooks)
                hook = hook.replace("amount", f"{amount}×")
                hook = hook.replace("ore", f"**{ore}**")
                await ctx.send(f"⛏️ +{xp_gained} XP | " + hook)

                await update_materials(ctx.author.id, ore, amount, ctx)
                await handle_mining_xp(ctx.author.id, xp_gained, ctx.guild.get_member(ctx.author.id), ctx.guild)
                
        else:
            await ctx.send("❌ | You must run `;start` first!")

class MaterialError(Exception):
    pass

role_levels = {
            802597628759375913 : 1,
            802599362885582879 : 2,
            802599364013850698 : 3,
            802601524257095700 : 4,
            802601869503365151 : 5,
            802602269324345346 : 6,
            802602115180134431 : 7,
        }

async def handle_mining_xp(uid, amount_added, member, guild):
    async with aiosqlite.connect('snp.db') as conn:
        async with conn.execute(f"SELECT mining, mining_xp FROM skill_levels WHERE uid = {uid};") as count:
            current_amount = await count.fetchall()
    if current_amount == []:
        async with aiosqlite.connect('snp.db') as conn:
            await conn.execute(f"insert into skill_levels values({uid}, 1, 1, {amount_added}, 0)") ############### UPDATE IF ADD MORE SKILLS
            await conn.commit()
    else:
        current_amount = current_amount[0]
        current_level = int(current_amount[0])
        current_xp = int(current_amount[1])
        max_xp = h.max_xp_skills(current_level)
        current_xp += amount_added
        if current_level != 7:
            if current_xp >= max_xp:
                mining_roles = list(role_levels.keys())
                for role in member.roles:
                    if role.id in mining_roles:
                        current_role = role.id
                        current_mining_level = role_levels[role.id]
                
                new_level = current_mining_level + 1

                await member.remove_roles(guild.get_role(current_role))
                new_role = guild.get_role(mining_roles[new_level-1])
                await member.add_roles(new_role)

                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"update skill_levels set mining_xp = 0, mining = {new_level} where uid = {uid};")
                    await conn.commit()
                
            else:
                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"update skill_levels set mining_xp = {current_xp} where uid = {uid};")
                    await conn.commit()

async def update_materials(uid, material, amount_added, chan = None):
    if type(material) == str:
        material = material.title()
        async with aiosqlite.connect('snp.db') as conn:
            async with conn.execute(f"SELECT amount FROM materials WHERE uid = {uid} and item_name = '{material}';") as count:
                current_amount = await count.fetchall()
        if current_amount == []:
            if amount_added < 0:
                raise MaterialError
            else:
                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"insert into materials values({uid}, '{material}', {amount_added})")
                    await conn.commit()
        else:
            current_amount = current_amount[0][0]
            if current_amount == 0:
                if amount_added < 0:
                    raise MaterialError
                else:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {amount_added} where uid = {uid} and item_name = '{material}'")
                        await conn.commit()
            else:
                if current_amount+amount_added < 0:
                    raise MaterialError
                else:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {current_amount+amount_added} where uid = {uid} and item_name = '{material}'")
                        await conn.commit()
    elif type(material) == list:
        for mat in material: # check if they have enough of each, raise an error if they don't
            index = material.index(mat)
            mat = mat.title()
            
            async with aiosqlite.connect('snp.db') as conn:
                async with conn.execute(f"SELECT amount FROM materials WHERE uid = {uid} and item_name = '{mat}';") as count:
                    current_amount = await count.fetchall()
            if current_amount == []:
                if amount_added[index] < 0:
                    raise MaterialError
            else:
                current_amount = current_amount[0][0]
                if current_amount == 0:
                    if amount_added[index] < 0:
                        raise MaterialError
                else:
                    if current_amount+amount_added[index] < 0:
                        raise MaterialError
        
        for mat in material: # Now apply them
            index = material.index(mat)
            mat = mat.title()
            async with aiosqlite.connect('snp.db') as conn:
                async with conn.execute(f"SELECT amount FROM materials WHERE uid = {uid} and item_name = '{mat}';") as count:
                    current_amount = await count.fetchall()
            if current_amount == []:
                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"insert into materials values({uid}, '{mat}', {amount_added[index]})")
                    await conn.commit()
            else:
                current_amount = current_amount[0][0]
                if current_amount == 0:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {amount_added[index]} where uid = {uid} and item_name = '{mat}'")
                        await conn.commit()
                else:
                    async with aiosqlite.connect('snp.db') as conn:
                        await conn.execute(f"update materials set amount = {current_amount+amount_added[index]} where uid = {uid} and item_name = '{mat}'")
                        await conn.commit()

                    
        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(mining(bot))
