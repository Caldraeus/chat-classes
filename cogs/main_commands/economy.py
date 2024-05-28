from email import message
from json.encoder import INFINITY
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
import asyncio

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
            "jamba juice" : 5000,
            "snake oil" : 10,
            "nft": 50,
            "map": 175
        }

        # Items that only a trader can buy.
        self.items_trader = {
            "snake oil",
            "nft",
            "map"
        }

        self.hidden_items = {
            "demon cookie" : 500,
            "scrap": 1,
            "boom bot" : 0,
            "gold spitter" : 0,
            "goober gobber" : 0,
            "fredster" : 0,
            "scrapbot" : 0,
            "yoinker" : 0
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
            embed.add_field(name=f"Jamba Juice | {self.items.get('jamba juice')} G", value="The *most* powerful and holy liquid... jamba juice! Removes all negative status effects when used!", inline=False)
            await ctx.send(embed=embed)
        if page == "trader":
            embed = discord.Embed(title=f"💸 Trader Shop 💸", colour=discord.Colour.from_rgb(166, 148, 255))
            embed.set_thumbnail(url="https://img.icons8.com/cotton/2x/shop--v3.png")
            embed.add_field(name=f"Snake Oil | {self.items.get('snake oil')} G", value=f'Snake oil! Super useful, very needed!', inline=False)
            embed.add_field(name=f"NFT | {self.items.get('nft')} G", value=f'Ah, a Non-Fungible Token! Use to gain some gold! ... probably.', inline=False)
            embed.add_field(name=f"Map | {self.items.get('map')} G", value=f'This dusty old piece of paper has a treausre map! Gives you a quest, plus some XP!', inline=False)
            await ctx.send(embed=embed)
            
    @commands.command()
    @commands.guild_only()
    async def use(self, ctx, *, item: str = None):
        if item:
            item = item.lower()

            try:
                target = ctx.message.mentions[0]
                
                str_mention = str(target.mention)

                item = item.replace(str_mention, "").strip()
                item = item.replace(str_mention[:2] + "!" + str_mention[2:], "").strip()
            except IndexError:
                target = None

            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select amount from inventory where uid = {ctx.author.id} and item_name = '{item.lower()}'") as u_info:
                    user_info = await u_info.fetchone()

            if item in self.items or item in self.hidden_items:


                if user_info != None:

                    current_amount = user_info[0]

                    if ctx.author.id in self.bot.server_boosters:
                        max_ap = 40
                    else:
                        max_ap = 20
                    #### Item handling. This, unfortunately, is going to be a very long if statement mess. Since I plan to add a large variety of items, with many different effects, it has to be this way.
                    ####

                    # NOTE: You'll notice I remove the item in each individual if statement. This is because of how some
                    # items are only removed after a delayed effect, etc.
                    
                    speaker = ctx.author.id
                    negative_effects = h.effects_negative
                    positive_effects= h.effects_positive

                    if item == "coffee":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("☕ | You drink your coffee... it's delicious! Now you have a bit more energy. (+2 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 2
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "monster":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("<:monster:739176788629913739> | You drink your monster energy... it's energizing! Now you have a bit more energy. (+6 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 6
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "adrenaline":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("💉 | You inject a vial of pure adrenaline... WOOO! **NOW YOU HAVE A LOT MORE ENERGY!**. (+10 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 10
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "demon cookie":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("🍪 | You munch on Lord Greymuul's homemade chocolate chip cookies... Wait a minute, these are raisins! How demonic! You're filled with rage. (+20 AP).")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 20
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                    elif item == "hot dog":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
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
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("👁️ | You 👍︎⚐︎☠︎💧︎🕆︎💣︎☜︎ your delectable ✞︎□︎✋︎👎︎. Golly, that sure was 👎︎☜︎☹︎♓︎👍︎✋︎⚐︎⬧︎! (+20 AP | +20 Shatter)")
                        new_ap = self.bot.users_ap[str(ctx.author.id)] + 20
                        if new_ap > max_ap:
                            new_ap = max_ap
                        self.bot.users_ap[str(ctx.author.id)] = new_ap
                        await h.add_effect(ctx.author, self.bot, "shatter", 20)
                    elif item == "milk":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
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
                                    removed = 100
                                await ctx.send(f"🥛 | You drink a cold glass of milk. You feel a lot better! (-{removed} {effect_cleansing.title()})") 
                            except IndexError:
                                await ctx.send(f"🥛 | You drink a cold glass of milk. You don't feel any different.")
                    elif item == "jamba juice":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        must_remove = []
                        if speaker in self.bot.user_status:
                            for status in self.bot.user_status[speaker]:
                                if status[0] in negative_effects:
                                    must_remove.append(status)
                                    # we Can't remove it here

                            for status in must_remove:
                                await h.handle_stacks(self.bot, status, speaker, INFINITY)

                            await ctx.send("<:jambajuice:798725534472339516> | You drink a delicous jamba juice! You feel great! (Negative status effects cleansed).")
                        else:
                            await ctx.send("<:jambajuice:798725534472339516> | You drink a delicous jamba juice! ... but nothing happens.")
                    elif item == "snake oil": # Gives a random status effect
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        chosen_status = random.choice(list(h.effect_list.keys()))
                        amount = random.randint(1, 10)

                        await ctx.send(f"🐍 | You drink your delicious and useful snake oil! Wait, what the hell was in this stuff!? (+{amount} **{chosen_status.title()}**)")
                        await h.add_effect(ctx.author, self.bot, chosen_status, amount)
                    elif item == "nft": # 80% chance to gain gold, 20% chance to lose gold.
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        cog = self.bot.get_cog('trader')
                        if self.bot.users_classes[str(ctx.author.id)] in cog.trader_classes:
                            await ctx.send("Woah there buddy, as a Trader, you wouldn't lay a finger on NFT's, since they're a scam and all. Try selling them to someone instead!")
                        else:
                            amount = random.randint(100, 500)
                            chance = random.randint(1, 100)

                            if chance <= 20:
                                await ctx.send(f"🐒 | You take your NFT and... oh shit, you got scammed! You lose {amount} G.\n\nAnd for even trying to use an NFT, you also lose that same amount in coolness.")
                                await h.add_gold(ctx.author.id, -amount, self.bot)
                            else:
                                await ctx.send(f"🐒 | You take your NFT and... do whatever people do with NFT's! It's a success! You gain {amount} G.\n\nBut honestly? NFT's suck. That's why you just lost that same amount in coolness.")
                                await h.add_gold(ctx.author.id, amount, self.bot)

                            await h.add_coolness(ctx.author.id, -amount)
                    elif item == "map": # gives user a quest
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        xp_amount = random.randint(100, 2000)
                        await ctx.send(f"🗺️ | You search over your map... (+{xp_amount} XP)")
                        await h.xp_handler(ctx.author, ctx.message, self.bot, boost = xp_amount)
                        await h.fetch_random_quest(ctx.message, self.bot, override=True)
                    elif item == "scrap":
                        await ctx.send("You... use your scrap? Yeah, you use your scrap. I guess you sort of just... bang the pieces together? It's really annoying. People tell you to stop. Hell, the scrap even breaks after you do that. Nice going, idiot. (-10 **Coolness**)")
                        await h.add_coolness(ctx.author.id, -10)
                    elif item == "boom bot":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("🤖 | You release your boom bot into the wild... I wonder where it'll end up?")
                        await asyncio.sleep(random.randint(15, 3600))
                        def check(m: discord.Message):
                            return m.author and m.author.id != ctx.author.id and m.guild.id == ctx.guild.id and ctx.author.id != self.bot.user.id and m.author.bot != True and m.channel.id == ctx.channel.id
                            
                        response_message = await self.bot.wait_for('message', check=check)
                        target = response_message.author
                        await response_message.channel.send(f"**💥[EXPLOSION!]💥 + 500 Coolness** | KABOOM!! **{ctx.author.mention}**'s Boom Bot rolls up and explodes on **{target.display_name}**. ")
                        await h.add_coolness(ctx.author.id, 500)
                    elif item == "gold spitter":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)

                        personal_gold = random.randint(100,3000)
                        others_gold = random.randint(10, 1000)

                        await ctx.send(f"🤖 | You activate your gold spitter... woah, look out! The gold spitter spits **{personal_gold}** gold at you, and **{others_gold}** gold around the area!")
                        await h.add_gold(ctx.author.id, personal_gold, self.bot)
                    
                        def check(m: discord.Message):
                            return m.author and m.author.id != ctx.author.id and m.guild.id == ctx.guild.id and ctx.author.id != self.bot.user.id and m.author.bot != True

                        response_message = await self.bot.wait_for('message', check=check)
                        response_target = response_message.author

                        await response_message.channel.send(f"**{response_target.display_name}** picks up the remaining **{others_gold} G** left behind by {ctx.author.display_name}!")
                        await h.add_gold(response_target.id, others_gold, self.bot)
                    elif item == "goober gobber":
                        if target and target != ctx.author:
                            if str(target.id) in self.bot.users_classes.keys():
                                await ctx.send(f"🤖 | You activate your goober gobber. Oh, god! It goobs it's gobbers all over **{target.display_name}**! (+10 **Goobered**)")
                                await h.remove_items(speaker, self.bot, item.lower(), 1)
                                await h.add_effect(target, self.bot, "goobered", 10)
                            else:
                                await ctx.send(f"🤖 | You activate your goober gobber. Oh, god! It goobs it's gobbers all over **{target.display_name}**! But wait... they're immune, because they're classless! Curses!")
                        else:
                            await ctx.send("⚠️ | Hey there, this is a targeted item! Try mentioning a target after you use it! For example, `;use bomb @God#9876`")
                    elif item == "fredster":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        await ctx.send("<:fredster:956297087253897226> | Holy shit! Is that a Fredster? Man, look at him go! Wow. Just wow.\n\nHonestly that was incredible. So incredible, in fact, you feel... inspired! | **(+25 Inspired)**")
                        await h.add_effect(ctx.author, self.bot, "inspired", 25)
                    elif item == "yoinker":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        if target and target != ctx.author:
                            if str(target.id) in self.bot.users_classes.keys():
                                try:
                                    async with aiosqlite.connect('main.db') as conn:
                                        async with conn.execute(f"select item_name from inventory where uid = {target.id};") as chan:
                                            stuff = await chan.fetchall()

                                    stolen_item = random.choice(stuff[0])
                                    
                                    await h.remove_items(target.id, self.bot, stolen_item, 1)
                                    await h.alter_items(ctx.author.id, ctx, self.bot, stolen_item, change = 1)
                                    await ctx.send(f"🤏 | Your yoinker reaches into **{target.display_name}**'s pocket, yoinking their **{stolen_item.title()}**! It's all yours now.")
                                except IndexError:
                                    await ctx.send(f"🤏 | Your yoinker attempts to yoink! But alas, **{target.display_name}** has no yoinkables to yoink yet! Better luck next time!")
                            else:
                                await ctx.send(f"🤏 | Your yoinker attempts to yoink! But alas, **{target.display_name}** has no yoinkables to yoink yet! Better luck next time!")
                    elif item == "scrapbot":
                        await h.remove_items(speaker, self.bot, item.lower(), 1)
                        scrap_created = random.randint(5,20)
                        await ctx.send(f"🤖 | Your scrapbot spits some more scrap out! Wait... if you used scrap to make the bot, where did it get more scrap from? Weird. **(+{scrap_created} Scrap)**")
                        await h.alter_items(ctx.author.id, ctx, self.bot, "scrap", scrap_created)
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
                    if item in self.items and item not in self.items_trader:  
                        await h.alter_items(ctx.author.id, ctx, self.bot, item.lower(), amount, self.items[item.lower()]*amount)
                    elif item in self.items and item in self.items_trader:  
                        if self.bot.users_classes[str(ctx.author.id)] == "trader":
                            await h.alter_items(ctx.author.id, ctx, self.bot, item.lower(), amount, self.items[item.lower()]*amount)
                        else:
                            await ctx.send("⚠️ | Hey, you can't buy this item! Come back when you're a trader or higher!")
                    else:
                        await ctx.send("⚠️ | That item doesn't exist. Did you make a typo?")
                    
                else:
                    await ctx.send("⚠️ | You forgot to specify what you'd like to buy!")
            else:
                await ctx.send("⚠️ | That's an invalid amount of items!")
        except ValueError:
            await ctx.send("⚠️ | You need to specify how many you'd like to buy! (Ex. `;buy 1 hot dog`).")
    
    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx): # ctx.author.id in self.bot.users_factions.keys()
        try:
            daily_amount = 100
            faction_pts = 10
            if ctx.author.id in self.bot.claimed: # or ctx.author.id == 340222819680124929 or ctx.author.id == 740308712450818079:
                await ctx.send("❌ | You've already claimed your daily gift this rollover! Use `;rollover` to check when you can claim again.")
            else:
                mss = ""

                if self.bot.users_classes[str(ctx.author.id)] == "pacted": # Classes that directly alter the daily gold go first.
                    if await h.get_demon(ctx.author.id, self.bot) == "trokgroor":
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select * from users where id = '{ctx.author.id}';") as info:
                                user = await info.fetchone()
                        level = user[8] - 19
                        daily_amount = daily_amount+(level*50)
                        if(ctx.author.id in self.bot.users_factions.keys()):
                            f_id = self.bot.users_factions[ctx.author.id]
                            if ctx.author.id in self.bot.server_boosters:
                                mss += f"✅ | You and Trokgroor print {2*daily_amount} gold!"
                            else:
                                mss += f"✅ | You and Trokgroor print {daily_amount} gold!"
                elif ctx.author.id in self.bot.server_boosters: # Our default gold thing goes last.
                    mss += f"✅ | You gained {daily_amount*2} gold!"
                else:
                    mss += f"✅ | You gained {daily_amount} gold!"

                if(ctx.author.id in self.bot.users_factions.keys()): # Faction points are their own thing.
                    f_id = self.bot.users_factions[ctx.author.id]
                    if ctx.author.id in self.bot.server_boosters:
                        await h.give_faction_points(ctx.author.id, f_id, faction_pts*2)
                        mss += f"\n\n*(+{faction_pts*2} Faction Points!)*"
                    else:
                        await h.give_faction_points(ctx.author.id, f_id, faction_pts)
                        mss += f"\n\n*(+{faction_pts} Faction Points!)*"

                if self.bot.users_classes[str(ctx.author.id)] == "adventurer": # Additional daily rewards are calculated here.
                    mss += "\n\n⚔️ | You also gain 10 AP, 25x Inspired, and 1x Jamba Juice!"
                    await h.add_effect(ctx.author, self.bot, "inspired", 25)
                    await h.alter_items(ctx.author.id, ctx, self.bot, "jamba juice", 1)
                    self.bot.users_ap[str(ctx.author.id)] += 10
                
                await h.add_gold(ctx.author.id, daily_amount, self.bot)
                self.bot.claimed.append(ctx.author.id)
                await ctx.send(mss)
        except (TypeError, KeyError):
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
