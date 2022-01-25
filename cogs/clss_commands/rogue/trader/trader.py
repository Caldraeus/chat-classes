import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
from asyncio import TimeoutError
import aiosqlite

class trader(commands.Cog): # It is worth noting that this class has a lot to do with the shop command, found in economy.py.
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(2, 1, commands.BucketType.user)
    async def trade(self, ctx, target: discord.Member = None): # Open a trade menu with someone.
        def check_author(m: discord.Message):
            return m.content and m.channel == ctx.message.channel and m.author.id == ctx.message.author.id

        def check_target(m: discord.Message):
            return m.content and m.channel == ctx.message.channel and m.author.id == target.id

        if target and target != ctx.author and target.id != 713506775424565370:
            if self.bot.users_classes[str(ctx.author.id)] == "trader":
                if (str(target.id) in list(self.bot.registered_users.keys())): # 1. Ask trader what to sell, 2. Ask trader how much they want for it, 3. Ask other use if they agree.
                    await ctx.send(f"{ctx.author.mention} | What item do you wish to trade?")
                    try:
                        item = await self.bot.wait_for('message', check=check_author, timeout=15)
                        item = item.content.lower()
                        async with aiosqlite.connect('main.db') as conn:
                            async with conn.execute(f"select amount from inventory where uid = {ctx.author.id} and item_name = '{item.lower()}'") as u_info:
                                user_info = await u_info.fetchone()

                        if user_info != None:
                            await ctx.send(f"{ctx.author.mention} | How many do you wish to trade away?")
                            amount = await self.bot.wait_for('message', check=check_author, timeout=15)
                            try:
                                amount = int(amount.content)
                                current_amount = user_info[0]

                                if current_amount - amount < 0:
                                    await ctx.send("⚠️ | You don't have enough of that item!")
                                else:
                                    await ctx.send(f"{ctx.author.mention} | How much should {target.display_name} pay you?")
                                    gold = await self.bot.wait_for('message', check=check_author, timeout=15)
                                    gold = int(gold.content)

                                    await ctx.send(f"Okay! {target.mention}, do you agree to purchase **{amount}** {item.title()} for **{gold}** G? (YES or NO)")
                                    agree = await self.bot.wait_for('message', check=check_target, timeout=30)
                                    
                                    if agree.content.lower() == "yes":
                                        target_gold = await h.get_gold(target.id)
                                        if target_gold - gold < 0:
                                            await ctx.send(f"⚠️ | Unfortunately, **{target.display_name}** cannot afford this!")
                                        else:
                                            await h.add_gold(ctx.author.id, gold, self.bot)
                                            await h.add_gold(target.id, -gold, self.bot)
                                            await h.remove_items(ctx.author.id, self.bot, item.lower(), amount)
                                            await h.alter_items(target.id, ctx, self.bot, item.lower(), amount)
                                            await h.xp_handler(ctx.message, self.bot, boost = gold/2)
                                            await ctx.send(f"✅ | Trade complete! **{ctx.author.display_name}** gains {gold/2} XP!")
                                            if item == "nft":
                                                await h.award_ach(18, ctx.message.channel, ctx.author, self.bot)
                                    else:
                                        await ctx.send(f"{ctx.author.mention} | Your trade offer was declined!")

                            except ValueError:
                                await ctx.send("⚠️ | That's not a number!")
                            
                        else:
                            await ctx.send(f"⚠️ | It looks like you don't have any item called \"{item.title()}\". Did you make a typo?")

                    except TimeoutError:
                        await ctx.send("⚠️ | Woops, looks like you took too long. Try again!")

                else:
                    await ctx.send("⚠️ | Invalid trading target! You must target a user registered in the bot.")
                        
# A setup function the every cog has
def setup(bot):
    bot.add_cog(trader(bot)) 

"""
item = item.lower()
async with aiosqlite.connect('main.db') as conn:
    async with conn.execute(f"select amount from inventory where uid = {ctx.author.id} and item_name = '{item.lower()}'") as u_info:
        user_info = await u_info.fetchone()

if item in self.items or item in self.hidden_items:
    if user_info != None:

        current_amount = user_info[0]

-------------------------------------------
def check(m: discord.Message):
    return m.content and m.channel == ctx.message.channel and m.author.id in self.involved[ctx.guild.id]
try:
    chosen = await self.bot.wait_for('message', check=check, timeout=10)

"""