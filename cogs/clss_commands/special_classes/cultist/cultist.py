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
import aiohttp

class cultist(commands.Cog): # self.qualified_name
    def __init__(self, bot):
        self.bot = bot
        self.rituals = {}
        self.involved = {}
        self.hooks = [
            "Your prayers call to the void",
            "Your cries reach ancient evils",
            "You beckon the deep",
            "Your whisper to the darkness",
            "You call out to the fathomless void",
            "You reach your hand out the a great evil",
            "You pray to an unseen dementor",
            "Your cries beckon chaos"
        ]
    pass

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pray(self, ctx): # Costs 2 ap
        if self.bot.users_classes[str(ctx.author.id)] == "cultist goon":
            ap_works = await h.alter_ap(ctx.message, 10, self.bot)
            if ap_works:
                if ctx.guild.id not in self.rituals and ctx.guild.id not in self.involved:
                    self.rituals[ctx.guild.id] = 1
                    self.involved[ctx.guild.id] = []
                elif ctx.guild.id in self.rituals and ctx.guild.id in self.involved and self.rituals[ctx.guild.id] != 'active':
                    self.rituals[ctx.guild.id] += 1
                
                if ctx.author.id not in self.involved[ctx.guild.id]:
                    print("Not involved")
                    self.involved[ctx.guild.id].append(ctx.author.id)

                progress = self.rituals[ctx.guild.id]

                if progress == 1:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/7.png"
                elif progress == 2:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/6.png"
                elif progress == 3:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/5.png"
                elif progress == 4:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/4.png"
                elif progress == 5:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/3.png"
                elif progress == 6:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/2.png"
                elif progress == 7:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/1.png"
                elif progress == 8:
                    link = "http://kaktuskontainer.wdfiles.com/local--files/7/0.png"

                if progress < 8:
                    await ctx.send(f"*{random.choice(self.hooks)}... ({progress}/8)*")
                    await ctx.send(link)
                if progress >= 8 and progress != 'active':
                    ritual_choice = random.randint(1,1)
                    self.rituals[ctx.guild.id] = 'active'
                    if ritual_choice == 1: # Cookies 
                        await ctx.send("**THE GROUND BEGINS TO REND, AS AN ANCIENT EVIL IS RELEASED...**")
                        await asyncio.sleep(3)
                        await ctx.send("**...THE SKY BEGINS TO WHIRL AND GROW A DARK RED. THE WORLD IS GRIPPED WITH FEAR. A CREVICE OPENS UP IN FRONT OF THE CULTISTS...**")
                        await asyncio.sleep(3)
                        await ctx.send("**...AS HIS HIGHNESS, LORD GREYMUUL OF THE SEVENTH SANCTUM, ARISES!**")
                        await asyncio.sleep(3)
                        async with aiohttp.ClientSession() as session:
                            # testhook = await ctx.channel.create_webhook(name="Test")
                            url = await h.webhook_safe_check(ctx.channel)
                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await hook.send(content="**WHO DARES RAISE ME FROM MY SLUMBER?**", username="Lord Greymuul, King of Demons", avatar_url="https://store-images.microsoft.com/image/apps.37024.13510798884682687.3563fce5-fc8b-4f80-b38f-f4e9de7d37f5.c9f36a6c-08d0-46aa-9911-0492259e6df3?mode=scale&q=90&h=300&w=300")
                            await asyncio.sleep(6.5)
                            await hook.send(content="**SILENCE! LEST YOU WISH TO BE TORN TO SHREDS.**", username="Lord Greymuul, King of Demons", avatar_url="https://store-images.microsoft.com/image/apps.37024.13510798884682687.3563fce5-fc8b-4f80-b38f-f4e9de7d37f5.c9f36a6c-08d0-46aa-9911-0492259e6df3?mode=scale&q=90&h=300&w=300")
                            await asyncio.sleep(5)
                            await hook.send(content="**I BELIEVE I UNDERSTAND NOW. YOU THERE - CULTISTS - I ADMIRE YOUR BRAVERY IN SUMMONING ME. ALLOW ME TO REWARD SUCH BRAVERY WITH A GIFT.**", username="Lord Greymuul, King of Demons", avatar_url="https://store-images.microsoft.com/image/apps.37024.13510798884682687.3563fce5-fc8b-4f80-b38f-f4e9de7d37f5.c9f36a6c-08d0-46aa-9911-0492259e6df3?mode=scale&q=90&h=300&w=300")
                            await asyncio.sleep(5)
                            await ctx.send("*Lord Greymuul carefuly hands each cultist a cookie...*")
                            for cultdude in self.involved[ctx.guild.id]:
                                await h.alter_items(cultdude, ctx, self.bot, "demon cookie", 1)
                                await asyncio.sleep(.5)
                            await hook.send(content="**THERE YOU ARE. NOW ENJOY IT, AS YOUR LIFE IS SHORT. GOODBYE, MORTALS!**", username="Lord Greymuul, King of Demons", avatar_url="https://store-images.microsoft.com/image/apps.37024.13510798884682687.3563fce5-fc8b-4f80-b38f-f4e9de7d37f5.c9f36a6c-08d0-46aa-9911-0492259e6df3?mode=scale&q=90&h=300&w=300")
                            await asyncio.sleep(5)
                        await ctx.send("Lord Greymuul slips back down through the crack in the ground, and all returns to normal.")
                        
                    self.involved[ctx.guild.id] = []
                    self.rituals[ctx.guild.id] = 0
    
            


# A setup function the every cog has
def setup(bot):
    bot.add_cog(cultist(bot))
