import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
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
                embed = discord.Embed(title="", colour=discord.Colour(0x2c2f33), description="")


                if progress == 1:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/7.png")
                elif progress == 2:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/6.png")
                elif progress == 3:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/5.png")
                elif progress == 4:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/4.png")
                elif progress == 5:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/3.png")
                elif progress == 6:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/2.png")
                elif progress == 7:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/1.png")
                elif progress == 8:
                    embed.set_image(url="http://kaktuskontainer.wdfiles.com/local--files/7/0.png")

                if progress < 8:
                    await ctx.send(f"*{random.choice(self.hooks)}... ({progress}/8)*", embed=embed)
                if progress >= 8 and progress != 'active':
                    ritual_choice = random.randint(1,4)
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
                        await ctx.send("*Lord Greymuul slips back down through the crack in the ground, and all returns to normal.*")
                    elif ritual_choice == 2: # Business Demon
                        await ctx.send("*A slow, brooding fog begins to spread around the cultists...*")
                        await asyncio.sleep(3)
                        await ctx.send("*...The temperature lowers, as their vision begins to cloud...*")
                        await asyncio.sleep(3)
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(ctx.channel)
                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await hook.send(content="*Ahhh.... Hello there...*", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                            await asyncio.sleep(5)
                            chosen_cultist = ctx.message.guild.get_member(random.choice(self.involved[ctx.guild.id]))
                            await hook.send(content=f"*Hey, hey... {chosen_cultist.mention}... lets make a deal...*", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"*I'll make you richhhhh... in exchange for your fellow cultists sufferinggg...*", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"***Do we have a deal...?***", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                            
                            def check(m: discord.Message):
                                return m.content and m.channel == ctx.message.channel and m.author.id == chosen_cultist.id

                            try:
                                chosen = await self.bot.wait_for('message', check=check, timeout=20)
                                chosen = chosen.content.lower()
                                affirmative = ['yes', 'sure', 'deal', 'yeah', 'ye', 'yea', 'yep', 'yup', 'okay']
                                if chosen in affirmative:
                                    await hook.send(content=f"*Heh heh... a pleasure doing busines...*", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                                    await asyncio.sleep(4)
                                    gold_gained = random.randint(500,1000)
                                    coolness_lost = random.randint(500,1000)
                                    await ctx.send(f"As Xoth sinks back into the fog, {chosen_cultist.mention} finds that they are holding a bag of {gold_gained} gold! However, the other cultists involved all lose that same amount. That was really uncool, dude! So uncool, that you also lost {coolness_lost} coolness for betraying your fellow cultists. Shame on you.")
                                    for cultdude in self.involved[ctx.guild.id]:
                                        if cultdude == chosen_cultist.id:
                                            await h.add_coolness(cultdude, -coolness_lost)
                                            await h.add_gold(cultdude, gold_gained, self.bot)
                                        else:
                                            await h.add_gold(cultdude, -gold_gained, self.bot)
                                        await asyncio.sleep(.5)
                                else:
                                    await hook.send(content=f"*Hehhhhh... Your lossssss...*", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                                    await asyncio.sleep(4)
                                    coolness_gained = random.randint(500,1000)
                                    await ctx.send(f"As Xoth sinks away, you all thank {chosen_cultist.mention} for not throwing you under the bus. This display of camaraderie was pretty frickin' cool, and all cultists involved gain +{coolness_gained} coolness!")
                                    for cultdude in self.involved[ctx.guild.id]:
                                        await h.add_coolness(cultdude, coolness_gained)
                                        await asyncio.sleep(.5)        
                            except:
                                await hook.send(content=f"*Hehhhhh... You bore me...*", username="Xoth, The Barterer", avatar_url="https://i.pinimg.com/600x315/84/1c/fb/841cfb6504c3c7677bfc8d722b4e7234.jpg")
                    elif ritual_choice == 3: # Hot Dog Monster
                        await ctx.send("*The summoning circle pulsates as...* ***A LARGE FLESHY HAND GRIPS THE SIDE!***") 
                        await asyncio.sleep(4)
                        await ctx.send("***A LARGE FLESHY BEAST PULLS HIMSELF OUT OF THE SUMMONING CIRCLE!***")
                        await asyncio.sleep(4)
                        await ctx.send("***OH GOD, OH FUCK! IT'S THE HOTDOG DEMON! PANIC!***")
                        await asyncio.sleep(3)
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(ctx.channel)
                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await hook.send(content=f"**KILLLLLLL MEEEEEEEE!!!!**", username="THE HOTDOG DEMON", avatar_url="https://images-cdn.9gag.com/photo/aO7e1BN_700b.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"**WHY WAS I CREATED? WHAT KIND OF SICK JOKE IS MY LIFE?! AAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!**", username="THE HOTDOG DEMON", avatar_url="https://images-cdn.9gag.com/photo/aO7e1BN_700b.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"**MY FLESH BURNS, THE WORLD TREMBLES - I CRAVE THE MEATS OF THOSE LOST TO THE DEEP. AAAAAAAAAAAAAAAAAAA!!!!!**", username="THE HOTDOG DEMON", avatar_url="https://images-cdn.9gag.com/photo/aO7e1BN_700b.jpg")
                            await asyncio.sleep(5)
                            chosen_cultist = ctx.message.guild.get_member(random.choice(self.involved[ctx.guild.id]))
                            await ctx.send(f"*The Hotdog Demon grabs {chosen_cultist.mention} and begins regurgitating hotdogs all over them.*")
                            await asyncio.sleep(5)
                            await hook.send(content=f"**I'M TOO PERFECT! TOO PERFECT FOR THIS WORLD! AAAAAAAAAAAAAAAAAAAA!!!**", username="THE HOTDOG DEMON", avatar_url="https://images-cdn.9gag.com/photo/aO7e1BN_700b.jpg")
                            await asyncio.sleep(5)
                            await ctx.send(f"*The Hotdog Demon then melts all over {chosen_cultist.mention}, leaving 5 hotdogs behind, which {chosen_cultist.mention} picks up.*")
                            await h.alter_items(chosen_cultist.id, ctx, self.bot, "hot dog", 5)
                    elif ritual_choice == 4: # Riddle Demon - https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg
                        await ctx.send("The ground rumbles... as the floor opens up beneath the cultists!")
                        await asyncio.sleep(4)
                        await ctx.send("They find themselves in a large cave... full of webs!")
                        await asyncio.sleep(4)
                        await ctx.send("Oh no, this is the lair of Maxeena, The Riddle Demon!")
                        await asyncio.sleep(4)
                        async with aiohttp.ClientSession() as session:
                            url = await h.webhook_safe_check(ctx.channel)
                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                            await hook.send(content=f"*Ahhhhhh.... wellllllcome....*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"*It seemsssssss that you have fallen into my web....*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"*Hehehehehahahahaha...*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            await asyncio.sleep(5)
                            await hook.send(content=f"*Heyyyyyyy..... riddle me thisssss.....*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            await asyncio.sleep(5)
                            riddle_chosen = random.randint(1,5)
                            if riddle_chosen == 1:
                                await hook.send(content=f"*What hasssss to be broken before you can usssse it...?*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            elif riddle_chosen == 2:
                                await hook.send(content=f"*What month of the year hassssssss 28 dayssssss...?*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            elif riddle_chosen == 3:
                                await hook.send(content=f"*A man who wassssss outssssside in the rain without an umbrella or hat didn’t get a ssssingle hair on his head wet. Why?*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            elif riddle_chosen == 4: 
                                await hook.send(content=f"*I sssssshave every day, but my beard sssstaysssss the ssssame. What am I?*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            elif riddle_chosen == 5:
                                await hook.send(content=f"*The perssssson who makesss it hasss no need of it; the person who buyssss it has no usssse for it. The person who usesss it can neither see nor feel it. What issss it?*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                            
                            

                            def check(m: discord.Message):
                                    return m.content and m.channel == ctx.message.channel and m.author.id in self.involved[ctx.guild.id]
                            try:
                                chosen = await self.bot.wait_for('message', check=check, timeout=10)
                                
                                chosen = chosen.content.lower()
                                correct = False
                                
                                if riddle_chosen == 1 and 'egg' in chosen:
                                    correct = True
                                elif riddle_chosen == 2 and ("every" in chosen or "all" in chosen):
                                    correct = True
                                elif riddle_chosen == 3 and ("bald" in chosen or "no hair" in chosen):
                                    correct = True
                                elif riddle_chosen == 4 and ("barber" in chosen or "hair cut" in chosen):
                                    correct = True
                                elif riddle_chosen == 5 and ("coffin" in chosen or "grave" in chosen):
                                    correct = True

                                if correct:
                                    await hook.send(content=f"*Hehhhhh.... correcttt....*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                                    await ctx.send("Maxeena laughs sinisterly, as a fog surrounds the cultists...")
                                    await asyncio.sleep(4)
                                    await ctx.send("The cultists find themself back on the surface. Hey, getting that riddle correct was pretty cool! Everyone involved gains 500 coolness!")
                                    for cultdude in self.involved[ctx.guild.id]:
                                        await h.add_coolness(cultdude, 500)
                                        await asyncio.sleep(.5)

                                else:
                                    await hook.send(content=f"*You.... are.... wrong...*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                                    await asyncio.sleep(4)
                                    await ctx.send("Suddenly, Maxeena attacks all the cultists! They barely make it out alive, but in the process, lose 500 coolness!")
                                    for cultdude in self.involved[ctx.guild.id]:
                                        await h.add_coolness(cultdude, -500)
                                        await asyncio.sleep(.5)
                            except:
                                await hook.send(content=f"*Too slowww....*", username="Maxeena, The Riddle Demon", avatar_url="https://i.pinimg.com/736x/3e/9e/6f/3e9e6f85b636bb178f7ad4228d9c3b80.jpg")
                                await asyncio.sleep(4)
                                await ctx.send("Suddenly, Maxeena attacks all the cultists! They barely make it out alive, but in the process, lose 500 coolness!")
                                for cultdude in self.involved[ctx.guild.id]:
                                    await h.add_coolness(cultdude, -500)
                                    await asyncio.sleep(.5)

                    self.involved[ctx.guild.id] = []
                    self.rituals[ctx.guild.id] = 0
    
            


# A setup function the every cog has
def setup(bot):
    bot.add_cog(cultist(bot))
