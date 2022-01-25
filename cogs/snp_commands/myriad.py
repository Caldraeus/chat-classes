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
from fancy_text import fancy

class myriad(commands.Cog): #TODO: Implement faction race commands, and the ability to set faction requirements.
    def __init__(self, bot):
        self.bot = bot
        self.gambling = []
        self.force_jackpot = False
        self.slot_values = {
            '🍅' : [1, 1.75, 3.75],
            '💀' : [0.05, 0.025, 0],
            '💀' : [0.05, 0.025, 0],
            '💀' : [0.05, 0.025, 0],
            '💀' : [0.05, 0.025, 0],
            '💀' : [0.05, 0.025, 0],
            '💀' : [0.05, 0.025, 0],
            '🥓' : [1.5, 2, 3.5],
            '🥓' : [1.5, 2, 3.5],
            '🥓' : [1.5, 2, 3.5],
            '🥓' : [1.5, 2, 3.5],
            '🔥' : [.5, .25, 0.125],
            '🔥' : [.5, .25, 0.125],
            '🔥' : [.5, .25, 0.125],
            '<a:wooyeah:804905363140247572>' : [2, 3, 5.5],
            '🍇' : [0.5, 0.3, 1.5],
            '🍇' : [0.5, 0.3, 1.5],
            '🍇' : [0.5, 0.3, 1.5],
            '🍇' : [0.5, 0.3, 1.5],
            '🍄' : [1, 1.5, 2.75],
            '🍋' : [1.75, 2, 2.25],
            '<a:jackpot:804920508982099988>' : [2, 4, 'jackpot'],
            '<a:jackpot:804920508982099988>' : [2, 4, 'jackpot'],
            '🍆' : [0.0125, 0.00625, 0.003125],
            '🍆' : [0.0125, 0.00625, 0.003125],
            '🍆' : [0.0125, 0.00625, 0.003125],
            '<:zombo:804914906012319754>' : [1, 0.5, 0.25],
            '🍌' : [.5, 1,5],
            '🍌' : [.5, 1,5],
            '🍌' : [.5, 1,5],
        }   

        self.jackpot = 100000

    def is_in_guild(guild_id):
        async def predicate(ctx):
            return ctx.guild and ctx.guild.id == guild_id
        return commands.check(predicate)

    def is_in_cat(cat_id):
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.category_id == cat_id
        return commands.check(predicate)

    def is_in_chan(chan):
        async def predicate(ctx):
            return ctx.channel.id and ctx.channel.id == chan
        return commands.check(predicate)


    pass # EOF
        
    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    @commands.is_owner()
    async def setjackpot(self, ctx, num: int):
        await ctx.send("Jackpot value updated.")
        self.jackpot = num
    
    @commands.command()
    @commands.is_owner()
    async def forcejackpot(self, ctx):
        await ctx.send("Jackpot rate increased.")
        self.force_jackpot = True

    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    @is_in_cat(802630421920612354)
    async def jackpot(self, ctx):
        await ctx.send(f'💸 | The current jackpot is **{self.jackpot}** gold! Good luck!')

    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    @is_in_cat(802630421920612354)
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def slots(self, ctx, wager: int):
        if wager < 50:
            await ctx.send("The minimum wager for slots is 50 gold!")
        else:
            original = wager
            await h.add_gold(ctx.author.id, -wager, self.bot, debt_mode = False, purchase_mode = ctx, boost_null = True)
            slots = list(self.slot_values.keys())
            random.shuffle(slots)

            results = {}

            rig_chance = random.randint(1,25)

            if self.force_jackpot == True:
                self.force_jackpot = False
                slot_1 = '<a:jackpot:804920508982099988>'
                slot_2 = '<a:jackpot:804920508982099988>'
                slot_3 = '<a:jackpot:804920508982099988>'
            else:
                if rig_chance != 1:
                    slot_1 = random.choice(slots)
                    slot_2 = random.choice(slots)
                    slot_3 = random.choice(slots)
                else:
                    slot_1 = '💀'
                    slot_2 = '💀'
                    slot_3 = '💀'

            results[slot_1] = 1
            if slot_2 in results.keys():
                results[slot_1] = 2
            else:
                results[slot_2] = 1

            if slot_3 in results.keys():
                results[slot_3] = results[slot_3] + 1
            else:
                results[slot_3] = 1


            if list(results.keys())[0] == "<a:jackpot:804920508982099988>" and results['<a:jackpot:804920508982099988>'] == 3:
                await ctx.send(f"{ctx.author.mention}\n<:STEASnothing:517873442381627392>   **__SLOTS__** **\n-=[{slot_1}|{slot_2}|{slot_3}]=-\n---------------------**\n\nYou won the jackpot! Enjoy the {self.jackpot} G!")
                await h.add_gold(ctx.author.id, self.jackpot, self.bot, debt_mode = False, purchase_mode = ctx, boost_null = True)
                
                embed = discord.Embed(title="💸 Jackpot Payout 💸", colour=discord.Colour.from_rgb(147,112,219), description="Someone has won the jackpot!", timestamp=datetime.now())
                
                embed.add_field(name="Amount", value=self.jackpot)
                embed.add_field(name="Winner", value=ctx.author.mention, inline=True)

                chan = ctx.guild.get_channel(802631294075928597)

                await chan.send(embed=embed)

                self.jackpot = 100000
            else:

                for item in results.keys():
                    amount = results[item]
                    if item == '<a:wooyeah:804905363140247572>':
                        payout_change = self.slot_values[item]
                        payout_change = payout_change[amount-1]
                        wager += wager*payout_change
                        await h.add_effect(ctx.author, self.bot, "wooyeah", amount = amount*3)
                    if item != "<a:jackpot:804920508982099988>":
                        payout_change = self.slot_values[item]
                        payout_change = payout_change[amount-1]

                        wager *= payout_change

                wager = round(wager)
                if wager < original:
                    self.jackpot += (original-wager)
                
                await ctx.send(f"{ctx.author.mention}\n<:STEASnothing:517873442381627392>   **__SLOTS__** **\n-=[{slot_1}|{slot_2}|{slot_3}]=-\n---------------------**\n\nYou got back {wager} G!")
                await h.add_gold(ctx.author.id, wager, self.bot, debt_mode = False, purchase_mode = ctx, boost_null = True)


    @commands.command()
    @commands.guild_only()
    @is_in_guild(732632186204979281)
    @is_in_cat(802630421920612354)
    async def blackjack(self, ctx, amount: int): # Activity: 1
        if amount <= 0:
            await ctx.send("Nice try, bucko. Use a positive number.")
        else:
            try:
                await h.add_gold(ctx.author.id, -amount, self.bot, debt_mode = False, purchase_mode = ctx, boost_null = True)
                if ctx.author.id not in self.gambling:
                    self.gambling.append(ctx.author.id)
                    ai_types = ["aggro", "safe", "balanced"]*3
                    ai_types.append("cheat")
                    ai_type = random.choice(ai_types)

                    end = False

                    def check(m: discord.Message):
                        return m.content and m.channel == ctx.message.channel and m.author.id == ctx.author.id

                    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10]*4

                    def deal(deck):
                        random.shuffle(deck)
                        card = random.choice(deck)
                        deck.remove(card)
                        return card

                    chosen = ""
                    user_hand = [deal(deck), deal(deck)]
                    ai_hand = [deal(deck), deal(deck)]

                    await ctx.send(content=ctx.author.mention, embed=gen_embed(user_hand, ai_hand, amount))
                    chosen = await self.bot.wait_for('message', check=check, timeout=60)
                    
                    ai_stand = False
                    user_stand = False

                    if chosen.content.lower() == "stand":
                        user_stand = True

                    while ai_stand == False or user_stand == False:
                        if user_stand == False:
                            user_hand.append(deal(deck))

                        if ai_type == "aggro":
                            if sum(ai_hand) < 17:
                                ai_hand.append(deal(deck))
                            else:
                                ai_stand = True
                        elif ai_type == "safe":
                            if sum(ai_hand) < 15:
                                ai_hand.append(deal(deck))
                            else:
                                ai_stand = True
                        elif ai_type == "balanced":
                            if sum(ai_hand) < 13:
                                ai_hand.append(deal(deck))
                            else:
                                coin_toss = random.randint(1,2)
                                if coin_toss == 1:
                                    ai_stand = True
                                else:
                                    if sum(ai_hand) < 16:
                                        ai_hand.append(deal(deck))
                                    else:
                                        ai_stand = True
                        elif ai_type == "cheat": # Like a true casino, we are rigged.
                            if sum(ai_hand) != 21:
                                ai_hand = gen_fake_hand(ai_hand[0], deck, ai_hand)
                            elif sum(ai_hand) == 21:
                                ai_stand = True

                        if sum(user_hand) > 21:
                            await ctx.send(f"**[BUST!]** | You drew {user_hand[-1]} and busted! You lost {amount} G!")
                            break
                        elif sum(ai_hand) > 21:
                            fhand = ""
                            for i in range(len(ai_hand)):
                                if i != len(ai_hand)-1:
                                    fhand += f"**{ai_hand[i]}** + "
                                else:
                                    fhand += f"**{ai_hand[i]}**"
                            await ctx.send(f"**[ANNAISHA BUST!]** | SHIT! I busted! You gained {2*amount} G!\n\n(My hand was: [{sum(ai_hand)}] {fhand})")
                            await h.add_gold(ctx.author.id, amount*2, self.bot, boost_null = True)
                            break
                        
                        if user_stand == False:
                            await ctx.send(content=ctx.author.mention, embed=gen_embed(user_hand, ai_hand, amount))
                            chosen = await self.bot.wait_for('message', check=check)
                            if chosen.content.lower() == "stand":
                                user_stand = True
                            else:
                                pass
                    
                    fhand = ""
                    for i in range(len(ai_hand)):
                        if i != len(ai_hand)-1:
                            fhand += f"**{ai_hand[i]}** + "
                        else:
                            fhand += f"**{ai_hand[i]}**"

                    if ai_stand == True and user_stand == True: 
                        if ai_type == "cheat" and sum(user_hand) != 21:
                            await ctx.send(f"**[LOSS!]** | Haha, get fucked! I won! You lost {amount} G!\n\n(My hand was: [{sum(ai_hand)}] {fhand})")
                        elif ai_type == "cheat" and sum(user_hand) == 21:
                            await ctx.send(f"**[TIE!]** | You tied! You didn't lose or gain any gold!\n\n(My hand was: [{sum(ai_hand)}] {fhand})")
                            await h.add_gold(ctx.author.id, amount, self.bot, boost_null = True)
                        elif sum(user_hand) > sum(ai_hand):
                            await ctx.send(f"**[WIN!]** | Damn, you won! You earned {amount*2} G!\n\n(My hand was: [{sum(ai_hand)}] {fhand})")
                            await h.add_gold(ctx.author.id, amount*2, self.bot, boost_null = True)
                        elif sum(user_hand) < sum(ai_hand):
                            await ctx.send(f"**[LOSS!]** | Haha, get fucked! I won! You lost {amount} G!\n\n(My hand was: [{sum(ai_hand)}] {fhand})")
                        elif sum(user_hand) == sum(ai_hand):
                            await ctx.send(f"**[TIE!]** | Damn, we tied! Your gold amount stays the same!\n\n(My hand was: [{sum(ai_hand)}] {fhand})")
                            await h.add_gold(ctx.author.id, amount, self.bot, boost_null = True)
                    self.gambling.remove(ctx.author.id)
            except SyntaxError:
                pass
        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(myriad(bot))

def gen_embed(hand, ai_hand, wager):
    embed = discord.Embed(title="Blackjack", colour=discord.Colour.from_rgb(147,112,219), description=f"Wager: {wager}\nPlease say **hit** or **stand**.")
    
    ai_cards = f"**{ai_hand[0]}** +"
    for card in range((len(ai_hand))-1):
        ai_cards += "<:card:804545542171918348>"
    
    fhand = ""
    for i in range(len(hand)):
        if i != len(hand)-1:
            fhand += f"**{hand[i]}** + "
        else:
            fhand += f"**{hand[i]}**"

    embed.add_field(name="Your Hand", value=fhand+f"\nTotal: {sum(hand)}", inline=True)
    embed.add_field(name="My Hand", value=ai_cards, inline=True)

    return embed


def gen_fake_hand(start, deck, hand):
    amount_remaining = 21
    for card in hand:
        amount_remaining -= card
    hit_zero = False
    if amount_remaining <= 10:
        hand.append(amount_remaining)

    else:
        if 10 in deck:
            hand.append(10)
        else:
            if 9 in deck:
                deck.append(9)
    
    return hand
