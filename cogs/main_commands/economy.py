import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
import matplotlib.pyplot as plt
from jishaku.functools import executor_function
from io import BytesIO

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = {
            "coffee" : 50,
            "hot dog" : 75,
            "monster" : 125,
            "adrenaline" : 225,
            "void" : 275,
            "milk" : 1000,
            "jamba juice" : 5000
        }

        self.hidden_items = {
            "demon cookie" : 500
        }

    @commands.command()
    @commands.guild_only()
    async def shop(self, ctx, page = "consumables", number = 1):
        if page == "consumables" and number == 1:
            embed = discord.Embed(title=f"🍺 Consumables Shop 🍺", colour=discord.Colour.from_rgb(166, 148, 255))
            # embed.set_footer(text=f"Use {h.prefix}shop {page} page_number to see more!")
            embed.set_thumbnail(url="https://img.icons8.com/cotton/2x/shop--v3.png")
            embed.add_field(name=f"Coffee | {self.items.get('coffee')} G", value=f'A quick boost. Delicious and refreshing! Restores 2 AP.', inline=False)
            embed.add_field(name=f"Hot Dog | {self.items.get('hot dog')} G", value=f"A delicious hot dog. Restores 4 ap, and gives some coolness.", inline=False)
            embed.add_field(name=f"Monster | {self.items.get('monster')} G", value=f'A monster energy. Great if you ignore the kidney stones! Restores 6 AP.', inline=False)
            embed.add_field(name=f"Adrenaline | {self.items.get('adrenaline')} G", value="A pure vial of adrenaline. Very strong. Restores 10 AP.")
            embed.add_field(name=f"Void | {self.items.get('void')} G", value="Holy shit, where did I get this stuff? Restores 20 AP, but applies 20 stacks of shatter!", inline=False)
            embed.add_field(name=f"Milk | {self.items.get('milk')} G", value="A powerful liquid... milk. Removes up to 100 stacks of your most recent status effect when consumed!", inline=False)
            embed.add_field(name=f"Jamba Juice | {self.items.get('jamba juice')} G", value="The *most* powerful and holy liquid... jamba juice! Removes all status effects, good or bad, when consumed!", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def use(self, ctx, *, item: str = None):
        if item:
            item = item.lower()
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select inventory, gold from users where id = '{ctx.author.id}'") as u_info:
                    user_info = await u_info.fetchone()

            inv = user_info[0].split("|")
            gold = user_info[1]
            
            for owned_item in inv:
                new_guy = owned_item.split(",")
                inv[inv.index(owned_item)] = new_guy
            
            end = ""
            
            if [''] in inv:
                inv.remove(['']) # Temporary workaround.
            items = [item[0] for item in inv] # Array of just the names of the items in the 2D array.

            if item in self.items or item in self.hidden_items:
                if item in items:
                    if ctx.author.id in self.bot.server_boosters:
                        max_ap = 40
                    else:
                        max_ap = 20
                    #### Item handling. This, unfortunately, is going to be a very long if statement mess. Since I plan to add a large variety of items, with many different effects, it has to be this way.
                    ####
                    
                    if item == "coffee":
                        await ctx.send("☕ | You drink your coffee... it's delicious! Now you have a bit more energy. (+2 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 2
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "monster":
                        await ctx.send("<:monster:739176788629913739> | You drink your monster energy... it's energizing! Now you have a bit more energy. (+6 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 6
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "adrenaline":
                        await ctx.send("💉 | You inject a vial of pure adrenaline... WOOO! **NOW YOU HAVE A LOT MORE ENERGY!**. (+10 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 10
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "demon cookie":
                        await ctx.send("🍪 | You munch on Lord Greymuul's homemade chocolate chip cookies... Wait a minute, these are raisins! How demonic! You're filled with rage. (+20 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 20
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "hot dog":
                        if self.bot.users_classes[str(ctx.author.id)] == "pacted" and await h.get_demon(ctx.author.id, self.bot) == "foop": # Buffed dot hogs
                            async with aiosqlite.connect('main.db') as conn:
                                async with conn.execute(f"select * from users where id = '{ctx.author.id}';") as info:
                                    user = await info.fetchone()
                            level = user[8] - 19
                            await ctx.send(f"🌭 | You and Foop split a delicious hot dog. Ah, just like being at the faire with your best friend! (+{4+(level)} AP | +{10+(5*level)} Coolness)")
                            new_ap = self.bot.users_ap[str(ctx.author.id)] + 4+(level)
                            if new_ap > max_ap:
                                new_ap = max_ap
                            self.bot.users_ap[str(ctx.author.id)] = new_ap
                            await h.add_coolness(ctx.author.id, 10+(5*level))
                        else:
                            await ctx.send("🌭 | You eat your delicious hot dog. Ah, just like being at the faire! (+4 AP | +10 Coolness)")
                            new_ap = self.bot.users_ap[str(ctx.author.id)] + 4
                            if new_ap > max_ap:
                                new_ap = max_ap
                            self.bot.users_ap[str(ctx.author.id)] = new_ap
                            await h.add_coolness(ctx.author.id, 10)
                    elif item == "void":
                        await ctx.send("👁️ | You 👍︎⚐︎☠︎💧︎🕆︎💣︎☜︎ your delectable ✞︎□︎✋︎👎︎. Golly, that sure was 👎︎☜︎☹︎♓︎👍︎✋︎⚐︎⬧︎! (+20 AP | +20 Shatter)")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 20
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                        await h.add_effect(ctx.author, self.bot, "shatter", 20)
                    elif item == "milk":
                        speaker = ctx.author.id
                        if speaker not in self.bot.user_status:
                            self.bot.user_status[speaker] = []
                            await ctx.send(f"🥛 | You drink a cold glass of milk. You don't feel any different.")
                        else:
                            try:
                                effect_cleansing = self.bot.user_status[speaker][0][0]
                                self.bot.user_status[speaker][0][1] = self.bot.user_status[speaker][0][1] - 100
                                if self.bot.user_status[speaker][0][1] <= 0:
                                    removed = self.bot.user_status[speaker][0][1] + 100
                                    self.bot.user_status[speaker].remove(self.bot.user_status[speaker][0])
                                else:
                                    removed_amount = 100
                                await ctx.send(f"🥛 | You drink a cold glass of milk. You feel a lot better! (-{removed} {effect_cleansing.title()})") 
                            except IndexError:
                                await ctx.send(f"🥛 | You drink a cold glass of milk. You don't feel any different.")
                    elif item == "jamba juice":
                        await ctx.send("<:jambajuice:798725534472339516> | You drink a delicous jamba juice! You feel a helluva lot better! (Status effects cleansed)")
                        speaker = ctx.author.id
                        if speaker not in self.bot.user_status:
                            self.bot.user_status[speaker] = []
                        else:
                            self.bot.user_status[speaker] = []

                                
                    ####
                    ####
                    index = items.index(item)
                    
                    new_amount = int(inv[index][1]) - 1
                    
                    if new_amount > 0:
                        inv[index][1] = str(new_amount)
                        for sublist in inv:
                            if inv.index(sublist) == len(inv)-1:
                                end += f"{','.join(sublist)}"
                            else:
                                end += f"{','.join(sublist)}|"
                    else:
                        for sublist in inv:
                            if sublist[0] != item:
                                if inv.index(sublist) == len(inv)-1:
                                    end += f"{','.join(sublist)}"
                                else:
                                    end += f"{','.join(sublist)}|"


                    async with aiosqlite.connect('main.db') as conn:
                        await conn.execute(f"update users set inventory = '{end}' where id = '{ctx.author.id}';")
                        await conn.commit()
                else:
                    await ctx.send(f"You are not currently in posession of {item.title()}. Perhaps you made a typo?")
               
    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, amount, *, item: str = None):
        try:
            amount = int(amount)
            if amount >= 1:
                item = item.lower()
                if item:
                    if item in self.items:  
                        await h.alter_items(ctx.author.id, ctx, self.bot, item.lower(), amount, self.items[item.lower()]*amount)
                    else:
                        await ctx.send("That item doesn't exist. Did you make a typo?")
                    
                else:
                    await ctx.send("You forgot to specify what you'd like to buy!")
            else:
                await ctx.send("That's an invalid amount of items!")
        except:
            await ctx.send("You need to specify how many you'd like to buy! (Ex. `;buy 1 hot dog`).")
    
    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx): 
        try:
            # if self.bot.users_classes[str(ctx.author.id)] == "pacted" and await h.get_demon(ctx.author.id, self.bot) == "foop":
            if ctx.author.id in self.bot.claimed: # or ctx.author.id == 340222819680124929 or ctx.author.id == 740308712450818079:
                await ctx.send("❌ | You've already claimed your daily gift this rollover! Use `;rollover` to check when you can claim again.")
            else:
                if self.bot.users_classes[str(ctx.author.id)] == "pacted":
                    if await h.get_demon(ctx.author.id, self.bot) == "trokgroor":
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select * from users where id = '{ctx.author.id}';") as info:
                                user = await info.fetchone()
                        level = user[8] - 19
                        await h.add_gold(ctx.author.id, 100+(level*50), self.bot, True)
                        if ctx.author.id in self.bot.server_boosters:
                            await ctx.send(f"✅ | You and Trokgroor print {2*(100+(level*50))} gold!")
                        else:
                            await ctx.send(f"✅ | You and Trokgroor print {100+(level*50)} gold!")
                        self.bot.claimed.append(ctx.author.id)
                    else:
                        await h.add_gold(ctx.author.id, 100, self.bot, True)
                        if ctx.author.id in self.bot.server_boosters:
                            await ctx.send("✅ | You gained 200 gold!")
                        else:
                            await ctx.send("✅ | You gained 100 gold!")
                        self.bot.claimed.append(ctx.author.id)
                else:
                    await h.add_gold(ctx.author.id, 100, self.bot, True)
                    if ctx.author.id in self.bot.server_boosters:
                        await ctx.send("✅ | You gained 200 gold!")
                    else:
                        await ctx.send("✅ | You gained 100 gold!")
                self.bot.claimed.append(ctx.author.id)
        except (TypeError, KeyError) as e:
            await ctx.send("❌ | You need to run `;start` first!")
        
    @commands.command()
    @commands.guild_only()
    async def economy(self, ctx, exact: str = "Basic"):
        async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"SELECT SUM(gold), AVG(gold), MAX(gold) as sum_gold FROM users;") as t_g:
                    gold_stats = await t_g.fetchone()
        if exact == "exact":
            total_gold = gold_stats[0]
            avg_gold = gold_stats[1]
            max_gold = gold_stats[2]
        else:
            exact = "Basic"
            total_gold = h.simplify(gold_stats[0])
            avg_gold = h.simplify(gold_stats[1])
            max_gold = h.simplify(gold_stats[2])

        async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"SELECT level, AVG(gold) FROM users GROUP BY level;") as data:
                    u_data = await data.fetchall()
        
        x_values = [i[0] for i in u_data]
        y_values = [i[1] for i in u_data]

        buff = await get_graph(x_values, y_values)

        f_content = f"**Economy Information** - {exact.title()}\n\n__Total Gold In Circulation:__ {total_gold}\n__Average Gold Per User:__ {avg_gold}\n__Most Gold Owned By User:__ {max_gold}"
        await ctx.send(content=f_content, file=buff)
        
@executor_function # makes sync int
def get_graph(x_values, y_values):
    plt.cla()
    plt.plot(x_values, y_values)
    plt.xlabel('User Levels') 
    plt.ylabel('Average Gold') 
    plt.title('Average Gold Per Level') 
    buff = BytesIO()
    plt.savefig(buff, format='png')
    buff.seek(0)
    buff = discord.File(fp=buff, filename='graph.png')
    plt.close()
    return(buff)

# A setup function the every cog has
def setup(bot):
    bot.add_cog(economy(bot))
