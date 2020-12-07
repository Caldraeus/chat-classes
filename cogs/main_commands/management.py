import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command(aliases=['enable'])
    @commands.guild_only()
    async def enablecc(self, ctx): # Enables the bot
        if ctx.author.id == ctx.guild.owner.id or ctx.author.id == self.bot.owner_id:
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select id from servers where id = '{ctx.guild.id}';") as servers:
                    server_id = await servers.fetchone()
                    if server_id:
                        await ctx.send(f"Your server ({server_id[0]}) is already enabled!")
                    else:
                        self.bot.servers.append(ctx.message.guild.id)
                        print("Fresh server")
                        await conn.execute(f"insert into servers values('{ctx.guild.id}', '')")
                        await conn.commit()
                        await ctx.send(f"Chat Classes has been enabled on this server! Use `{h.prefix}safezone` to disable a channel for that bot, and `{h.prefix}classzone` to re-enable a channel.")
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def safezone(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select bchannels from servers where id = '{ctx.guild.id}'") as g:
                banned = await g.fetchone()
                banned = banned[0]
                banned = banned.split('|')
                if str(channel.id) not in banned: # This is redundant. But I'm keeping it here JUST IN CASE.
                    banned.append(str(channel.id))
                    self.bot.banned_channels.append(str(channel.id))
                    final = '|'.join(banned)
                    await conn.execute(f"update servers set bchannels = '{final}' where id = '{ctx.guild.id}'")
                    await conn.commit()
                    await ctx.message.add_reaction('✅')
                else: # See above comment.
                    await ctx.send("Channel is already disabled!")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def classzone(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select bchannels from servers where id = '{ctx.guild.id}'") as g:
                banned = await g.fetchone()
                banned = banned[0]
                banned = banned.split('|')
                if str(channel.id) in banned: # This is redundant. But I'm keeping it here JUST IN CASE.
                    banned.pop(banned.index(str(channel.id)))
                    self.bot.banned_channels.remove(str(channel.id))
                    final = '|'.join(banned)
                    await conn.execute(f"update servers set bchannels = '{final}' where id = '{ctx.guild.id}'")
                    await conn.commit()
                    await ctx.message.add_reaction('✅')
                else: # See above comment.
                    await ctx.send("Channel is already enabled!")

    @commands.command()
    @commands.guild_only()
    async def disclaimer(self, ctx):
        guild = ctx.guild
        await ctx.send(f"Greetings, members of {guild.name}! Before this bot is active, the owner must understand that this bot messes with chat quite a bit. This includes sending messages, deleting messages, and creating (temporary!) channels. This bot will not destroy your server, I promise. I would only recommend this bot for small servers with friends/etc. For more information on managing this bot and what it does, use `;help` and read on how to disable the bot in specific channels.\n\nNow that that is all said and done, I will need the server owner ({guild.owner.mention}) to say `{h.prefix}enablecc`\n\nAdditionally, this bot makes use of nickname permissions, and it needs the highest role in a guild to operate. If you do not feel comfortable doing this, I understand, but you should recognise that this bot will have less functionality.\n\nThat is all!")

    @commands.command()
    @commands.guild_only()
    async def about(self, ctx):
        profile = discord.Embed(title=f"Chat Classes About", colour=discord.Colour(0x6eaf0b), description="")
        ###
        ###
        profile.set_footer(text=f"Bot Latency: {math.ceil(round(self.bot.latency * 1000, 1))} ms", icon_url="")
        profile.add_field(name="Bot Version", value=self.bot.version, inline=False)
        profile.add_field(name="Creator", value=f'Caldraeus#1337', inline=False)
        profile.add_field(name="Library", value=f'discord.py', inline=False)
    
    
        await ctx.send(embed=profile)

    """
    @commands.command(aliases=['pks'])
    @commands.guild_only()
    async def packs(self, ctx, *, target: discord.Member = None):
        # TODO: Display inventory
        if not target:
            target = ctx.author  
        else:
            target = target

        usr = h.find_usr(target.id)

        if usr: 
            try:
                packs = usr[6].split("$")
                if packs[0] == '':
                    packs.remove('')
                    if packs[0] == '':
                        raise("Error for erroring.")
            except:
                await ctx.send("<:redtick:605424981245034511> | You have nothing in your pack inventory!")
                return
        
            embed = discord.Embed(colour=discord.Colour(0x353535), timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=target.avatar_url)
            embed.set_author(name=f"{target.name}'s Packs")
            for item in packs:
                i = packs.index(item)
                if i % 2 == 1:
                    embed.add_field(name=f"{item.title()} Packs", value=f'×{packs[i-1].title()}')

            embed.set_footer(text="To see your cards, run ;cards")

            await ctx.send(embed=embed)
        else:
            await ctx.send("<:redtick:605424981245034511> | Target user has not registered yet.")

    @commands.command(aliases=['o', 'unpack', 'openpack'])
    @commands.guild_only()
    @commands.cooldown(1, 0.3, BucketType.user) 
    async def open(self, ctx, cpack = "core"):
        # TODO: CHECK THAT THEY HAVE A PACK
        if h.remove_pack(ctx.author.id, cpack.lower()):
            msg = await ctx.send("<a:opening:605795855529803817> | Your pack is opening...")
            conn = sqlite3.connect(os.path.realpath('./main.db'))
            c = conn.cursor()
            if cpack.lower() != 'core' and cpack.lower() not in h.ratings:
                table = c.execute(f"select * from cards where expansion = '{cpack.title()}';")
            elif cpack.lower() in h.ratings:
                table = c.execute(f"select * from cards where rarity = '{cpack.title()}';")
            else:
                table = c.execute(f"select * from cards")
            
            elements = []

            for i in table:
                if i[5] > 0 or i[5] == -1:
                    elements.append(i)
            
            conn.close()

            length = len(elements)
            if length == 0:
                await ctx.send("Critical error.")
            bv = 1 / length
            weights = []
            felements = []
            for item in elements:
                r = item[4]
                felements.append(item[0])
                if r == 'Heirloom':
                    weights.append(bv / 350)
                elif r == "Legendary":
                    weights.append(bv / 100)
                elif r == "Epic":
                    weights.append(bv / 30)
                elif r == "Rare":
                    weights.append(bv / 5)
                elif r == "Uncommon":
                    weights.append(bv / 3)
                elif r == "Common":
                    weights.append(bv)

            balance = 1 / h.totalise(weights)
            weights = h.equalise(weights, balance)

            # for item, item2 in zip(elements, weights):
            #     print(f"{item[0]} :: {item2}")

            if h.totalise(weights) > 1.0:
                diff = h.totalise(weights) - 1
                weights[0] -= diff
            
            character = h.get_character(choice(felements, p=weights))
            h.add_character(ctx.author.id, character[0])

            if character[5] > 0:
                h.change_char("printed", character[5]-1, character[0])

            embed = h.char_embed(character)
            embed.set_author(name=f"You opened {character[0]}!", icon_url=ctx.author.avatar_url)

            await msg.edit(content=None, embed=embed)
            if character[4] == "Heirloom":
                channel = self.bot.get_channel(611199302978764800)
                await channel.send(f'{ctx.author.name} ({ctx.author.id}) opened an Heirloom - {character[0]}!')
        else:
            await ctx.send("<:redtick:605424981245034511> | You don't have any cardpacks of that type!")
    """

# A setup function the every cog has
def setup(bot):
    bot.add_cog(management(bot))
