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

class forage(commands.Cog): #TODO: Implement faction race commands, and the ability to set faction requirements.
    def __init__(self, bot):
        self.bot = bot
        self.growing = {}

        self.mine_hooks = [
            "You find some amount stuff while foraging in the forest!",
            "While foraging, you found amount stuff!",
            "After a day in the forest, you find amount stuff!",
            "Nice! You found amount stuff!",
            "You forage amount stuff.",
            "Your foraging expedition rewards you with amount stuff."
        ]

        self.growing = []

        self.growing_rates = {
            802609903989948486 : 300,
            802609829175885844 : 240,
            802609330939232267 : 180,
            802609213729669160 : 120,
            802609153965031425 : 100,
            802609075509526578 : 50,
            802608937064988713 : 10,
        }

        self.materials = {
            "stick" : None,
            "leaf" : None,
            "berry" : "Raspberry",
            "sapling" : "Tree",
            "mushroom" : "Hearty Shroom",
            "wood" : None,
            "cotton" : "Cotton",
            "egg" : "Poultry Plant",
            "toxinshroom" : "Concentrated Poison",
            "clover" : None,
            "apple" : "Apple Tree",
            "coolium fruit" : "Coolness",
            "honey" : None,
            "fossil" : None,
            "hardwood" : None,
            "pumpkin" : "Pumpkin",
            "bamboo" : "Bamboo",
            "pearl" : "Rarity Essence",
            "shell" : None,
            "life essence" : "Child",
            "vitashroom" : None,
            "strongsap" : None,
            "rusted part" : "Strange Machinery",
            "fallen star" : "Lunar Essence",
            "melon" : "Melon",
            "eldritch wood" : "Raw Void",
            "death essence" : None,
            "old scroll" : None,
            "astral gem" : None,
            "wisp" : "Sad Soul",
            "jazzshroom" : "Jazzed Up Mushroom",
            "once-was" : "Now-Is",
            "coolness essence" : "Coolness",
            "dragon bones" : None,
            "astral wood" : None
        }
        
    pass

    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)

    def is_in_cat():
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.category_id == 802606676510769152
        return commands.check(predicate)

    def is_in_chan(chan):
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.id == chan
        return commands.check(predicate)

    pass # EOF
        
        
    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    @is_in_chan(802607830187245569)
    async def plant(self, ctx, amount: int, *, material):
        material = material.title()
        if ctx.author.id in self.growing:
            await ctx.send("You already have an ongoing farming task! I'll mention you when it's all done!")
        else:
            member = ctx.guild.get_member(ctx.author.id)
            
            for role in member.roles:
                if role.id in self.growing_rates.keys():
                    growing_time = self.growing_rates[role.id]

            try:
                if material.lower() in self.materials.keys():
                    new_material = self.materials[material.lower()]
                    if new_material != None:
                        await update_materials(ctx.author.id, [material], [-amount], ctx)

                        self.growing.append(ctx.author.id)

                        await ctx.send(f"🪴 | You water your plot and wait for your material to grow! Your task will be done in {growing_time} minutes!")
                        await asyncio.sleep(growing_time*60) # growing_time*60
                        await ctx.send(f"{ctx.author.mention} : Your growing task has finished! (**{material}** ⮕ **{new_material}**)")
                        self.growing.remove(ctx.author.id)
                        while ctx.author.id in self.growing:
                            self.growing.remove(ctx.author.id)
                        if material == "coolium fruit":
                            await h.xp_handler(ctx.author, ctx.message, self.bot, boost = amount)
                        elif material == "coolness essence":
                            await h.xp_handler(ctx.author, ctx.message, self.bot, boost = amount*5)
                        else:
                            await update_materials(ctx.author.id, new_material, round(amount*1.5), ctx)
                    else:
                        await ctx.send("That material is unable to be further planted!")
                else:
                    await ctx.send("That material doesn't exist, or can't be planted! Did you make a typo?")
            except MaterialError as err:
                await ctx.send(f"You don't have enough of that material for this! You need at least **{amount}** {material} to plant!")
            

    @commands.command()
    @commands.guild_only() 
    @is_in_guild(732632186204979281)
    @is_in_cat()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def forage(self, ctx):
        ## Stuff rarities. I would do this in self, but I want the amount to change every time.
        stff_rarity_beginner = RelativeWeightedChoice((
            (2000, ["Stick", random.randint(3,30)]),
            (2000, ["Leaf", random.randint(10,30)]),
            (1950, ["Vine", random.randint(5,10)]),
            (1950, ["Water", random.randint(5,10)]),
            (1900, ["Berry", random.randint(5, 10)]),
            (700, ["Sapling", random.randint(2,10)]),
            (700, ["Mushroom", random.randint(2,5)]),
            (700, ["Wood", random.randint(2,5)]),
            (700, ["Cotton", random.randint(2,8)]),
            (500, ["Egg", random.randint(1,3)]),
            (500, ["Toxinshroom", random.randint(1,3)]),
            (500, ["Clover", random.randint(1,3)]),
            (100, ["Coolium Fruit", random.randint(100,500)]),
            (100, ["Apple", 1])
        ))

        stff_rarity_novice = RelativeWeightedChoice((
            (1600, ["Stick", random.randint(3,30)]),
            (1600, ["Leaf", random.randint(10,30)]),
            (1600, ["Vine", random.randint(5,10)]),
            (1600, ["Water", random.randint(5,10)]),
            (1600, ["Berry", random.randint(5, 10)]),
            (900, ["Sapling", random.randint(2,20)]),
            (900, ["Mushroom", random.randint(2,15)]),
            (900, ["Wood", random.randint(2,15)]),
            (900, ["Cotton", random.randint(2,18)]),
            (600, ["Egg", random.randint(1,13)]),
            (600, ["Toxinshroom", random.randint(1,13)]),
            (600, ["Clover", random.randint(1,13)]),
            (600, ["Coolium Fruit", random.randint(100,500)]),
            (175, ["Apple", random.randint(1,3)]),
            (175, ["Honey", random.randint(1,3)]),
            (175, ["Fossil", random.randint(1,3)]),
            (175, ["Hardwood", random.randint(1,3)]),
            (175, ["Pumpkin", random.randint(1,3)]),
            (175, ["Bamboo", random.randint(1,3)]),
            (175, ["Pearl", random.randint(1,3)])
        ))

        stff_rarity_advanced = RelativeWeightedChoice((
            (1400, ["Stick", random.randint(3,30)]),
            (1400, ["Leaf", random.randint(35,45)]),
            (1400, ["Vine", random.randint(5,10)]),
            (1400, ["Water", random.randint(5,10)]),
            (1400, ["Berry", random.randint(5, 10)]),
            (1000, ["Sapling", random.randint(2,20)]),
            (1000, ["Mushroom", random.randint(2,15)]),
            (1000, ["Wood", random.randint(2,15)]),
            (1000, ["Cotton", random.randint(2,18)]),
            (900, ["Egg", random.randint(1,13)]),
            (900, ["Toxinshroom", random.randint(1,13)]),
            (900, ["Clover", random.randint(1,13)]),
            (900, ["Coolium Fruit", random.randint(100,500)]),
            (500, ["Apple", random.randint(1,13)]),
            (500, ["Honey", random.randint(1,13)]),
            (500, ["Fossil", random.randint(1,13)]),
            (500, ["Hardwood", random.randint(1,13)]),
            (500, ["Pumpkin", random.randint(1,13)]),
            (500, ["Bamboo", random.randint(1,13)]),
            (500, ["Pearl", random.randint(1,13)]),
            (200, ["Shell", random.randint(1,2)]),
            (200, ["Life Essence", random.randint(1,2)]),
            (200, ["Vitashroom", random.randint(1,2)]),
            (200, ["Meteorite", random.randint(1,2)]),
            (200, ["Luckstone", random.randint(1,2)]),
        ))

        stff_rarity_expert = RelativeWeightedChoice((
            (900, ["Sapling", random.randint(2,20)]),
            (900, ["Mushroom", random.randint(2,15)]),
            (900, ["Wood", random.randint(2,15)]),
            (900, ["Cotton", random.randint(2,18)]),
            (1000, ["Egg", random.randint(10,23)]),
            (1000, ["Toxinshroom", random.randint(10,23)]),
            (1000, ["Clover", random.randint(10,23)]),
            (1000, ["Coolium Fruit", random.randint(100,500)]),
            (900, ["Apple", random.randint(5,13)]),
            (900, ["Honey", random.randint(5,13)]),
            (900, ["Fossil", random.randint(5,13)]),
            (900, ["Hardwood", random.randint(5,13)]),
            (900, ["Pumpkin", random.randint(5,13)]),
            (900, ["Bamboo", random.randint(5,13)]),
            (900, ["Pearl", random.randint(5,13)]),
            (450, ["Shell", random.randint(5,12)]),
            (450, ["Life Essence", random.randint(5,12)]),
            (450, ["Vitashroom", random.randint(5,12)]),
            (450, ["Meteorite", random.randint(5,12)]),
            (450, ["Luckstone", random.randint(5,12)]),
            (450, ["Strongsap", random.randint(5,12)])
        ))

        stff_rarity_master = RelativeWeightedChoice((
            (1000, ["Egg", random.randint(10,23)]),
            (1000, ["Toxinshroom", random.randint(10,23)]),
            (1000, ["Clover", random.randint(10,23)]),
            (1000, ["Coolium Fruit", random.randint(100,500)]),
            (900, ["Apple", random.randint(5,13)]),
            (900, ["Honey", random.randint(5,13)]),
            (900, ["Fossil", random.randint(5,13)]),
            (900, ["Hardwood", random.randint(5,13)]),
            (900, ["Pumpkin", random.randint(5,13)]),
            (900, ["Bamboo", random.randint(5,13)]),
            (900, ["Pearl", random.randint(5,13)]),
            (450, ["Shell", random.randint(5,12)]),
            (450, ["Life Essence", random.randint(5,12)]),
            (450, ["Vitashroom", random.randint(5,12)]),
            (450, ["Meteorite", random.randint(5,12)]),
            (450, ["Luckstone", random.randint(5,12)]),
            (450, ["Strongsap", random.randint(5,12)]),
            (100, ["Rusted Part", 1]),
            (100, ["Fallen Star", 1]),
            (100, ["Melon", 1]),
            (100, ["Eldritch Wood", 1]),
            (100, ["Death Essence", random.randint(1,4)]),
            (5, ["Old Scroll", 1])
            
        ))

        stff_rarity_legendary = RelativeWeightedChoice((
            (1000, ["Apple", random.randint(5,13)]),
            (1000, ["Honey", random.randint(5,13)]),
            (1000, ["Fossil", random.randint(5,13)]),
            (1000, ["Hardwood", random.randint(5,13)]),
            (1000, ["Pumpkin", random.randint(5,13)]),
            (1000, ["Bamboo", random.randint(5,13)]),
            (1000, ["Pearl", random.randint(5,13)]),
            (500, ["Shell", random.randint(5,12)]),
            (500, ["Life Essence", random.randint(5,12)]),
            (500, ["Vitashroom", random.randint(5,12)]),
            (500, ["Meteorite", random.randint(5,12)]),
            (500, ["Luckstone", random.randint(5,12)]),
            (500, ["Strongsap", random.randint(5,12)]),
            (250, ["Rusted Part", random.randint(1,10)]),
            (250, ["Fallen Star", random.randint(1,10)]),
            (250, ["Melon", random.randint(1,10)]),
            (250, ["Eldritch Wood", random.randint(1,10)]),
            (250, ["Death Essence", random.randint(1,14)]),
            (100, ["Old Scroll", random.randint(1,2)]),
            (100, ["Raw Void", random.randint(1,2)]),
            (100, ["Old Scroll", random.randint(1,20)]),
            (100, ["Wisp", random.randint(1,2)]),
            (100, ["Jazzshroom", random.randint(1,2)]),
            (100, ["Once-Was", random.randint(1,2)])  
        ))

        stff_rarity_gmaster = RelativeWeightedChoice((
            (1500, ["Shell", random.randint(5,12)]),
            (1500, ["Life Essence", random.randint(5,12)]),
            (1500, ["Vitashroom", random.randint(5,12)]),
            (1500, ["Meteorite", random.randint(5,12)]),
            (1500, ["Luckstone", random.randint(5,12)]),
            (1500, ["Strongsap", random.randint(5,12)]),
            (1250, ["Rusted Part", random.randint(1,10)]),
            (1250, ["Fallen Star", random.randint(1,10)]),
            (1250, ["Melon", random.randint(1,10)]),
            (1250, ["Eldritch Wood", random.randint(1,10)]),
            (1250, ["Death Essence", random.randint(1,14)]),
            (500, ["Old Scroll", random.randint(1,12)]),
            (500, ["Raw Void", random.randint(1,12)]),
            (500, ["Old Scroll", random.randint(1,12)]),
            (500, ["Wisp", random.randint(1,12)]),
            (500, ["Jazzshroom", random.randint(1,12)]),
            (500, ["Once-Was", random.randint(1,10)]),
            (500, ["Coolness Essence", random.randint(1,10)]),
            (500, ["Dragon Bones", random.randint(5,6)]),
            (500, ["Astral Wood"], random.randint(5,10))
        ))

        ##
        member = ctx.guild.get_member(ctx.author.id)
        if str(ctx.author.id) in self.bot.users_classes.keys():
            ap_works = await h.alter_ap(ctx.message, 2, self.bot)
            if ap_works:
                if ctx.channel.id == 802608884137197609:
                    stuff = stff_rarity_beginner()
                elif ctx.channel.id == 802610383021932574:
                    stuff = stff_rarity_novice()
                elif ctx.channel.id == 802610545172807750:
                    stuff = stff_rarity_advanced()
                elif ctx.channel.id == 802610643407470632:
                    stuff = stff_rarity_expert()
                elif ctx.channel.id == 802610900279754793:
                    stuff = stff_rarity_master()
                elif ctx.channel.id == 802610978637479976:
                    stuff = stff_rarity_legendary()
                elif ctx.channel.id == 802611108128358410:
                    stuff = stff_rarity_gmaster()
                
                amount = stuff[1]
                stuff = stuff[0]
                # max_xp_skills
                xp_gained = random.randint(5,20)

                hook = random.choice(self.mine_hooks)
                hook = hook.replace("amount", f"{amount}×")
                hook = hook.replace("stuff", f"**{stuff}**")
                await ctx.send(f"🍁 +{xp_gained} XP | " + hook)

                await update_materials(ctx.author.id, stuff, amount, ctx)
                await handle_forage_xp(ctx.author.id, xp_gained, ctx.guild.get_member(ctx.author.id), ctx.guild)
                
        else:
            await ctx.send("❌ | You must run `;start` first!")

class MaterialError(Exception):
    pass

role_levels = {
            802609903989948486 : 1,
            802609829175885844 : 2,
            802609330939232267 : 3,
            802609213729669160 : 4,
            802609153965031425 : 5,
            802609075509526578 : 6,
            802608937064988713 : 7,
        }

async def handle_forage_xp(uid, amount_added, member, guild):
    async with aiosqlite.connect('snp.db') as conn:
        async with conn.execute(f"SELECT foraging, foraging_xp FROM skill_levels WHERE uid = {uid};") as count:
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
                forage_roles = list(role_levels.keys())
                for role in member.roles:
                    if role.id in forage_roles:
                        current_role = role.id
                        current_forage_level = role_levels[role.id]
                
                new_level = current_forage_level + 1

                await member.remove_roles(guild.get_role(current_role))
                new_role = guild.get_role(forage_roles[new_level-1])
                await member.add_roles(new_role)

                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"update skill_levels set foraging_xp = 0, foraging = {new_level} where uid = {uid};")
                    await conn.commit()
                
            else:
                async with aiosqlite.connect('snp.db') as conn:
                    await conn.execute(f"update skill_levels set foraging_xp = {current_xp} where uid = {uid};")
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
    bot.add_cog(forage(bot))
