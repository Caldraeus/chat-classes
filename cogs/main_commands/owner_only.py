import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite

class owner_only(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def servers(self, ctx): # Just displays the amount of servers it is in... 75 here we come!
        await ctx.send(len(self.bot.guilds))

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def say(self, ctx, *, stuff): # Just displays the amount of servers it is in... 75 here we come!
        await ctx.message.delete()
        await ctx.send(stuff)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def fquest(self, ctx, target: discord.User = None):
        if target:
            await h.fetch_random_quest(ctx.message, self.bot, target, True)
        else:
            await h.fetch_random_quest(ctx.message, self.bot, override=True)
    
    @commands.command()
    @commands.is_owner()
    async def release(self, ctx, version, *, notes):
        channel = self.bot.get_channel(734108098129821757)
        embed = discord.Embed(title=f"❗ Version {version} Released! ❗", colour=discord.Colour.from_rgb(255,0,0), description=notes)
        mss = await channel.send(content="╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲\n\n<@&738883975954563132>\n\n", embed=embed)
        await mss.publish()

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
    bot.add_cog(owner_only(bot))
