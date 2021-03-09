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
from discord import Webhook, AsyncWebhookAdapter
from asyncio.exceptions import TimeoutError
import sqlite3
from datetime import datetime

class factions(commands.Cog): #TODO: Implement faction race commands, and the ability to set faction requirements.
    def __init__(self, bot):
        self.bot = bot
        self.factions = {}
        self.grace = False
        """
        Faction Index Keys
        (ex: self.factions[faction_id][0])
        
        0 = Owner ID (INT)
        1 = Faction Mods (STR LIST), can be ''
        2 = Description (STR)
        3 = Requirements (STR list split by | then ,) (ex: wealth,100|coolness,50|level,10|notclass,swordsman,apprentice|)
        4 = Funds (INT) (not update constantly)
        5 = Faction IMG (STR)
        6 = Faction RGB (STR split by | conv to int)
        7 = Faction Name (STR)
        8 = Points (INT)
        9 = Role ID (int)
        10 = Intro Message ID
        """

        conn = sqlite3.connect('unique.db')
        current_amount = conn.execute(f"select * from factions;")
        fcs = current_amount.fetchall()
        
        for faction in fcs: # (135410565135728641, '', 'A group devoted to defeating Shadows. Under the guise of a school club.', 'None', 0, 'https://i.imgur.com/DNzZMBd.jpg', '0|133|236', 'S.E.E.S.', 0, 802675914542153770, 1234567890)
            self.factions[int(faction[0])] = [faction[1], faction[2], faction[3], faction[4], faction[5], faction[6], faction[7], faction[8], faction[9], faction[10], faction[11]]

    pass

    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)

    def is_in_chan():
        channel_ids = [
            802673115406663690,
            802624171242815531,
            802670914025684993
        ]
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.id in channel_ids
        return commands.check(predicate)

    pass

    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    @commands.is_owner()
    async def cfa(self, ctx):
        print(self.factions)

    
    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    @commands.is_owner()
    async def genfaction(self, ctx, f_id: int = 0):
        def check(m: discord.Message):
            return m.content and m.channel == ctx.message.channel and m.author.id == ctx.author.id
        await ctx.send("Faction generation progress started.\n\nFaction ID?")

        chosen = await self.bot.wait_for('message', check=check, timeout=20)
        fac_id = int(chosen.content)
        
        await ctx.send("Faction Owner ID?")

        chosen = await self.bot.wait_for('message', check=check, timeout=20)
        owner_id = int(chosen.content)
        
        await ctx.send("Description?")
        chosen = await self.bot.wait_for('message', check=check, timeout=20)
        desc = chosen.content

        await ctx.send("Image link?")
        chosen = await self.bot.wait_for('message', check=check, timeout=20)
        img = chosen.content

        await ctx.send("RGB? (ex: 255|255|255)")
        chosen = await self.bot.wait_for('message', check=check, timeout=20)
        rgb = chosen.content

        await ctx.send("Name?")
        chosen = await self.bot.wait_for('message', check=check, timeout=20)
        name = chosen.content

        i_rgb = rgb.split("|")
        r = int(i_rgb[0])
        g = int(i_rgb[1])
        b = int(i_rgb[2])

        color = discord.Colour.from_rgb(r, g, b)

        role = await ctx.guild.create_role(name=name.lower(), color=color, hoist=True, mentionable = True)

        embed = discord.Embed(title=name, colour=color, description=desc, timestamp=datetime.now())

        embed.set_image(url=img)
        embed.set_author(name=F"ID : {fac_id}")
        
        embed.add_field(name="Members", value=1)
        leader = self.bot.get_user(owner_id)
        embed.add_field(name="Leader", value=leader.mention, inline=True)
        embed.add_field(name="Requirements", value=None, inline = False)

        chan = self.bot.get_channel(802653320450801734)
        mss = await chan.send(embed=embed)

        member = ctx.guild.get_member(owner_id)

        await member.add_roles(role)
        f_leader = ctx.guild.get_role(802722969763577877)
        await member.add_roles(f_leader)
        
        try:
            fless = ctx.guild.get_role(802619205715099748)
            await member.remove_roles(fless)
        except:
            print("User doesn't have factionless role despite having claimed they didn't")

        # INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);

        # Try to wipe in case they have info still
        try:
            self.bot.users_factions[owner_id] = fac_id
            async with aiosqlite.connect('unique.db') as conn:
                await conn.execute(f"DELETE FROM faction_members WHERE uid = {ctx.author.id};")
                await conn.commit()
        except SyntaxError:
            pass

        # Add to factions DB
        async with aiosqlite.connect('unique.db') as conn:
            await conn.execute(f"INSERT INTO factions VALUES ({fac_id}, {owner_id}, '', '{desc}', 'None', 0, '{img}', '{rgb}', '{name}', 0, {role.id}, {mss.id});")
            await conn.execute(f"insert into faction_members values ({owner_id}, {fac_id}, 0);")
            await conn.commit()
        self.factions[fac_id] = [owner_id, '', desc, "None", 0, img, rgb, name, 0, role.id, mss.id]


        await ctx.send("Role and temp channels created. Manual setup required for channels and role position.")

        
    @commands.command(aliases=["topf"])
    @commands.guild_only()
    async def topfactions(self, ctx):
        async with aiosqlite.connect('unique.db') as conn:
            async with conn.execute(f"SELECT faction_name, faction_points FROM factions ORDER BY faction_points DESC;") as count:
                info = await count.fetchall()
        
        final = ""
        num = 1
        for faction in info:
            if num == 6:
                break
            else:
                final += f"#{num} - {faction[0]} - {faction[1]} FP\n\n"
                num+=1

        profile = discord.Embed(title=f"🛡️ The Coolest Factions 🛡️", colour=discord.Colour.from_rgb(255,0,0), description=final)
        profile.set_thumbnail(url="http://pixelartmaker.com/art/346bdb0be18bdb3.png")
    
        await ctx.send(embed=profile)

    @commands.command()
    @commands.guild_only()
    async def contribute(self, ctx, amount: int, *, item: str):
        if item.lower() in list(list(zip(*self.bot.get_cog('crafting').materials_data))[0]):
            await ctx.send(f"You contribute {amount} **{item.title()}** to your faction! Thanks!")
        else:
            await ctx.send("That isn't a real material! Make sure to check your spelling!")


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def delfaction(self, ctx, f_id: int = 0, mem = None):
        if f_id in self.factions.keys():
            fac = self.factions[f_id]
            if mem:
                try:
                    leader = self.bot.get_user(int(fac[0]))
                except:
                    leader = "Unknown"
                
                embed = discord.Embed(title=fac[7], colour=discord.Colour(0xf5a623), description=fac[2], timestamp=datetime.now())

                embed.set_image(url=fac[5])
                embed.set_author(name="⏬ A Legendary Faction Has Fallen! ⏬")


                async with aiosqlite.connect('unique.db') as conn:
                    async with conn.execute(f"SELECT COUNT(*) FROM faction_members WHERE faction_in = {f_id};") as count:
                        members = await count.fetchall()
                
                embed.add_field(name="Members", value=members[0][0])
                embed.add_field(name="Leader", value=leader.mention, inline=True)

                chan = self.bot.get_channel(802588249037340692)
                await chan.send(embed=embed)
            else:
                pass
            
            leader = ctx.guild.get_member(int(fac[0]))
            f_leader = ctx.guild.get_role(802722969763577877)
            fac_role = ctx.guild.get_role(int(fac[9]))
            await fac_role.delete()
            await leader.remove_roles(f_leader)
            fless = ctx.guild.get_role(802619205715099748)
            await leader.add_roles(fless)
            

            del self.factions[f_id]

            async with aiosqlite.connect('unique.db') as conn:
                await conn.execute(f"update faction_members set faction_in = 0 AND contribution = 0 WHERE faction_in = {f_id};")
                await conn.execute(f"DELETE FROM factions WHERE faction_id = {f_id};")
                await conn.commit()

            try:
                intro_chan = self.bot.get_channel(802653320450801734)
                mss = await intro_chan.fetch_message(int(fac[10]))
                await mss.delete()
            except ValueError:
                print("Unable to find faction intro message.")

            # Reload user factions
            self.bot.users_factions = {}
            async with aiosqlite.connect('unique.db') as conn: # This code makes sure the bot is enabled, then also makes sure that the bot is in an enabled channel
                async with conn.execute(f"select * from faction_members;") as dudes:
                    members = await dudes.fetchall()
            
            for person in members:
                self.bot.users_factions[int(person[0])] = int(person[1])

            await ctx.send("Faction removed.")
        else:
            await ctx.send("Invalid faction ID")

    @commands.command()
    @commands.guild_only() 
    @is_in_guild(732632186204979281)
    @is_in_chan()
    async def joinfaction(self, ctx, f_id: int = 0):
        member = ctx.guild.get_member(ctx.author.id)
        if str(ctx.author.id) in self.bot.users_classes.keys():
            def check(m: discord.Message):
                return m.content and m.channel == ctx.message.channel and m.author.id == ctx.author.id

            fless = ctx.guild.get_role(802619205715099748)
            in_dead_faction = False

            if ctx.author.id in self.bot.users_factions.keys(): # Just in case an error happens
                print("user in a faction, is it dead?")
                if self.bot.users_factions[ctx.author.id] not in self.factions.keys():
                    print("yeah, dead faction")
                    async with aiosqlite.connect('unique.db') as conn:
                        await conn.execute(f"DELETE FROM faction_members WHERE uid = {ctx.author.id};")
                        await conn.commit()

                    await member.add_roles(fless)
                    in_dead_faction = True

            if (fless in ctx.author.roles) or in_dead_faction or self.grace == True: # check if they have the factionless role
                # Check if faction exists
                if f_id in self.factions.keys():
                    await ctx.send(f"You're about to join **{self.factions[f_id][7]}**! You won't be able to change your faction until after the current faction race is over!\n\nType `confirm` to confirm!")
                    chosen = await self.bot.wait_for('message', check=check, timeout=20)
                    if chosen.content.lower() == "confirm":
                        try:
                            reqs = self.factions[f_id][3]
                            if reqs != "None":
                                async with aiosqlite.connect('main.db') as conn:
                                    async with conn.execute(f"select * from users where id = '{ctx.author.id}';") as info:
                                        user = await info.fetchone()

                                reqs = reqs.split("|")
                                for item in reqs:
                                    reqs[reqs.index(item)] = item.split(",")
                                for req in reqs:
                                    if req[0] == "coolness":
                                        if int(req[1]) > int(user[5]):
                                            raise SyntaxError
                                    elif req[0] == "wealth":
                                        if int(req[1]) > int(user[3]):
                                            raise SyntaxError
                                    elif req[0] == "level":
                                        if int(req[1]) > int(user[8]):
                                            raise SyntaxError

                            f_role = ctx.guild.get_role(self.factions[f_id][9])
                            await member.add_roles(f_role)
                            await member.remove_roles(fless)
                            self.bot.users_factions[ctx.author.id] = f_id
                            async with aiosqlite.connect('unique.db') as conn:
                                await conn.execute(f"insert into faction_members values({ctx.message.author.id}, {f_id}, 0)")
                                await conn.commit()

                            async with aiosqlite.connect('unique.db') as conn:
                                async with conn.execute(f"SELECT intro_mss_id FROM factions WHERE faction_id = {f_id}") as f_info:
                                    faction_info = await f_info.fetchone()

                            message_id = int(faction_info[0])
                            intro_chan = self.bot.get_channel(802653320450801734)
                            mss = await intro_chan.fetch_message(message_id)
                            embed = mss.embeds[0]

                            async with aiosqlite.connect('unique.db') as conn:
                                        async with conn.execute(f"SELECT COUNT(*) FROM faction_members WHERE faction_in = {f_id};") as count:
                                            members = await count.fetchall()

                            embed.set_field_at(0, name = "Members", value = members[0][0], inline=False)
                            await mss.edit(embed=embed)
                            await ctx.send(f"<:check_yes:802233343704956968> | Congrats! You are now part of **{self.factions[f_id][7]}**!")
                        except SyntaxError:
                            await ctx.send("You do not meet the faction's requirements.")
                    else:
                        await ctx.send("❌ | Faction joining cancelled!")
                else:
                    await ctx.send("❌ | Invalid faction ID! Double check you've typed the proper ID!")
            else:
                await ctx.send("❌ | You are already in a faction. Wait until the grace period to leave your current faction!")
        else:
            await ctx.send("❌ | You must run `;start` first!")

class MaterialError(Exception):
    pass

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
    bot.add_cog(factions(bot))