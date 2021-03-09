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

class artifacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active = []
        self.used = []
    pass

    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    async def commence(self, ctx):
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select artifact from users where id = '{ctx.author.id}';") as info:
                uinfo = await info.fetchone()
        
        aid = uinfo[0]
        
        if aid != "None":
            await ctx.send("You already have an artifact. Try again after artifact reset!")
            await h.update_quest(ctx.message, 18, -1, self.bot, True)
        else:
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select completed_quests, currently_questing from users where id = '{ctx.author.id}';") as chan:
                    quest = await chan.fetchone()
                    if quest:
                        if quest[1] != 0: # If the user has a quest...
                            quest_id = quest[1] # Setting this as a variable to close the first connection.

            if ctx.author.id not in self.active and quest[1] == 18:
                self.active.append(ctx.author.id)
                async with aiosqlite.connect('unique.db') as conn:
                    async with conn.execute(f"select artifact_id from artifacts where owner_id = 0;") as info:
                        artifacts = await info.fetchall()
                available_artifacts = []
                for item in artifacts:
                    available_artifacts.append(item[0])

                if available_artifacts == []:
                    await ctx.send("Unfortunately, there is nothing left for me to give. Try again, in a month.")
                    await h.update_quest(ctx.message, 18, -1, self.bot)
                else:
                    quest = random.choice(available_artifacts)
                    lives = 3
                    def check(m: discord.Message):
                        return m.content and m.channel == ctx.message.channel and m.author.id == ctx.author.id
                    ##########################################################
                    ##########################################################
                    """
                    The way quests work is simple. Upon choosing a quest, we define a few things.
                    1. Action Manager (action_manager)
                        This acts as a return function to handle each action taken by the user, and return a new redirect location, if there is one.
                    2. Redirect Variable (redirect) 
                        Referred to by the while loop each time it's run through to find out where the user is.
                    3. Inventory (inventory)
                        A list of items the user picks up.
                    4. Lives (lives) (optional)
                        A set of lives a user has before they're kicked out of the quest. Not always enabled.
                    5. Turns (turns)
                        Checks how many actions a user takes. Used to limit them.
                    """
                    ##########################################################
                    ##########################################################
                    try:
                        if quest == 1: # Mantle of The Titans
                            ### Set up variables & action manager, which is most of the code
                            redirect = "home"
                            inventory = []
                            lives = 3
                            turns = 0
                            async def action_manager(place, choice, ctx):
                                home_actions = ["leave", "enter blue room", "enter red room", "inspect constellation", "enter black room"]
                                if place == "home":
                                    if choice in home_actions:
                                        if choice == "leave":
                                            await ctx.send("You leave the dungeon.")
                                            raise TimeoutError
                                        elif choice == "enter red room":
                                            return "red room"
                                        elif choice == "enter blue room":
                                            return "blue room"
                                        elif choice == "enter black room":
                                            return "black room"
                                        elif choice == "inspect constellation":
                                            await ctx.send("You inspect the constellatin of Gror, the Titan of Peace.\n\nInscribed below him is the following.\n\n**■■■ four■■ ●oor ●■●ll ●■■ ●ou fr■■, ■u■ fir●■ ●ou ●u●■ ■●■■ ■■■ ●●r■■●■'● cro■■꜀.**\n\nThere is nothing else of note.")
                                            return "home"
                                        else:
                                            return "home"
                                    else:
                                        await ctx.send("Invalid chocie.")
                                        return "home"

                                elif place == "red room":
                                    if choice == "take his crown":
                                        if "crown" not in inventory:
                                            inventory.append("crown")
                                            await ctx.send("You reach up and grab the crown of stars. To your surprise, it comes out of the wall. You pocket it.")
                                        else:
                                            await ctx.send("You already have the crown.")
                                        return place
                                    elif choice == "take his sword":
                                        await ctx.send("The room trembles as the constellation comes to life! With one swing, he slices you in half, killing you.")
                                        raise TimeoutError
                                    else:
                                        await ctx.send("Unsure of what to do, you return to the main room.")
                                        return "home"
                                elif place == "blue room":
                                    if choice == "take his spawn" or choice == "take his key":
                                        await ctx.send("The room trembles as the constellation comes to life! With one large slam, he crushes you, killing you.")
                                        raise TimeoutError
                                    else:
                                        await ctx.send("Unsure of what to do, you return to the main room.")
                                        return "home"
                                elif place == "black room":
                                    if choice == "enter the orange door":
                                        if "crown" in inventory:
                                            await ctx.send("You open the door, entering a large field.")
                                            return "exit"
                                        else:
                                            await ctx.send("You open the door, and a large blade flys out, impaling you through the stomach. Your last vision is a smiling face, as you slowly die.")
                                            raise TimeoutError
                                    elif "enter the" in choice:
                                        await ctx.send("You open the door and enter, finding yourself in a blank, small stone room. However, nothing happens. You turn to leave, but there is no longer a door there. You scream for help, but the only response is your own voice, echoing in the room. You sit down, and accept your fate.")
                                        raise TimeoutError
                                    else:
                                        await ctx.send("Unsure of what to do, you return to the main room.")
                                        return "home"

                            ###
                            async with aiohttp.ClientSession() as session:
                                url = await h.webhook_safe_check(ctx.channel)
                                hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                async with aiohttp.ClientSession() as session:
                                    url = await h.webhook_safe_check(ctx.channel)
                                    hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                    await hook.send(content="...", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                    await asyncio.sleep(6.5)
                                    await hook.send(content="Interesting...", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                    await asyncio.sleep(5)
                                    await hook.send(content="In all my years of watching over this place, no one has been bold enough to walk right to me...", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                    await asyncio.sleep(5)
                                    await hook.send(content=f"I assume you're here for it. The Mantle? I wish you luck, {ctx.author.mention}. It's not an easy path.", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                await asyncio.sleep(3)
                                await ctx.send(f"The wall behind Sef raises slowly, revealing a long corridor. Are you ready?\n\n`Yes`\n`No`")
                                chosen = await self.bot.wait_for('message', check=check)
                                chosen = chosen.content.lower()
                                if chosen != "yes":
                                    raise TimeoutError
                                else:
                                    ## Main Loop
                                    mss = None
                                    while redirect != "exit":
                                        if redirect == "home":
                                            mss = await ctx.send(f"||{ctx.author.mention}||\nYou are standing within a large chamber with a stone floor. The walls appear as the cosmos, complete with constellations. There are 2 exits on either side of the room.\n\n`1. Leave.\n2. Enter Blue Room\n3. Enter Red Room\n4. Inspect constellation\n5. Enter Black Room`") ######################################
                                        elif redirect == "red room":
                                            mss = await ctx.send('''
    You enter the red room. Within these walls lies a large constellation of *Fullmar,* Titan of Darkness.

    Inscribed on the wall is the following.

    **■■■ ▲▲▲▲■■ d▲▲▲ s■a▲▲ s■■ y▲▲ ▲▲■■, ■▲■ ▲▲▲s■ y▲▲ m▲s■ ■a■■ ■■■ da▲■■s■'s ▲▲▲■■₁.**

    `1. Leave`
    `2. Take his Crown`
    `3. Take his Sword`
                                                
                                        ''')

                                        elif redirect == "blue room":
                                            mss = await ctx.send('''
    You enter the blue room. Within these walls lies a large constellation of *Iadirix,* Titan of Light. His spawn, *Golmex*, lies below him.

    Inscribed on the wall is the following.

    **the ▲▲▲▲th ●▲▲▲ ●h●▲▲ ●et ●▲▲ ▲▲ee, b▲t ▲▲▲●t ●▲▲ ●▲●t t●ke the ●●▲ke●t'● ▲▲▲wn₂.**

    `1. Leave`
    `2. Take his Spawn`
    `3. Take his Key`
                                                
                                        ''')
                                        elif redirect == "black room":
                                            mss = await ctx.send('''
    You enter the black room. Here, there is no light. However, as you trudge forward, you see five doors.

    What do you do?

    `1. Leave`
    `2. Enter the red door`
    `3. Enter the blue door`
    `4. Enter the green door`
    `5. Enter the orange door`
    `6. Enter the black door`
                                                
                                        ''')
                                        chosen = await self.bot.wait_for('message', check=check, timeout=360)
                                        chosen = chosen.content.lower()
                                        redirect = await action_manager(redirect, chosen, ctx)
                                        if mss:
                                            await mss.delete()
                                    async with aiohttp.ClientSession() as session:
                                        url = await h.webhook_safe_check(ctx.channel)
                                        hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                        await hook.send(content="Ah... you've made it! So, what did you learn? Which Titan betrayed the others? The one different than the others?\n\n`1. Gror\n2. Fullmar\n3. Iadirix\n4. Golmex`", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                    # Gror
                                    chosen = await self.bot.wait_for('message', check=check, timeout=360)
                                    chosen = chosen.content.lower()
                                    if chosen != "gror":
                                        async with aiohttp.ClientSession() as session:
                                            url = await h.webhook_safe_check(ctx.channel)
                                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                            await hook.send(content="Tragic... throughout all that, you couldn't see the truth. You are blind just like they were. Goodbye.", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                        raise TimeoutError
                                    else:
                                        async with aiohttp.ClientSession() as session:
                                            url = await h.webhook_safe_check(ctx.channel)
                                            hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                            await hook.send(content="Incredible... you have the wisdom that the 12 titans lacked. Here, you deserve this.", username="Sef, The Last Titan", avatar_url="https://i.imgur.com/dWkRNdQ.png")
                                            await award_artifact(ctx, ctx.author.id, 1)
                                            self.active.remove(ctx.author.id)
                                            await h.update_quest(ctx.message, 18, -1, self.bot, True)
                        elif quest == 2:
                            async with aiohttp.ClientSession() as session:
                                url = await h.webhook_safe_check(ctx.channel)
                                hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                await hook.send(content="Heya, chap! Looking for an artifact I see! Here, I can give you this premium artifact made just by me!\n\nTrust me! You want an artifact of this power! Truly amazing! It'll make you cool! Rich! Powerful! It'll just cost you *a whole lot!*\n\nSo? Whaddya say?\n\n`1. Yes\n2. No`", username="Xolorth", avatar_url="https://i.imgur.com/lA8qSDe.jpg")
                            chosen = await self.bot.wait_for('message', check=check, timeout=360)
                            chosen = chosen.content.lower()  
                            if chosen == "yes":
                                async with aiohttp.ClientSession() as session:
                                    url = await h.webhook_safe_check(ctx.channel)
                                    hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                    await hook.send(content="Really? Now hot dog, you've got a sharp eye! I'll just take **6660 Coolness** and **6660 Gold!** Enjoy, my fleshy fella!", username="Xolorth", avatar_url="https://i.imgur.com/lA8qSDe.jpg")
                                await h.add_coolness(ctx.author.id, -6660)
                                await h.add_gold(ctx.author.id, -6660, self.bot, True)
                                await award_artifact(ctx, ctx.author.id, 2)
                                await h.update_quest(ctx.message, 18, -1, self.bot, True)
                            else:
                                async with aiohttp.ClientSession() as session:
                                    url = await h.webhook_safe_check(ctx.channel)
                                    hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                                    await hook.send(content="A shame! A darn shame! Oh, well! Bye now!", username="Xolorth", avatar_url="https://i.imgur.com/lA8qSDe.jpg")
                                    self.active.remove(ctx.author.id)
                                    await h.update_quest(ctx.message, 18, -1, self.bot)
                    except TimeoutError:
                        self.active.remove(ctx.author.id)
                        await h.update_quest(ctx.message, 18, -1, self.bot)
            else:
                pass

    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    async def activate(self, ctx):
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select artifact from users where id = '{ctx.author.id}';") as info:
                uinfo = await info.fetchone()
        
        aid = uinfo[0]
        
        if aid != "None":
            if ctx.author.id in self.used:
                await ctx.send("You already used your artifact today!")
            else:
                self.used.append(ctx.author.id)
                async with aiosqlite.connect('unique.db') as conn:
                    async with conn.execute(f"select * from artifacts where artifact_id = {aid};") as info:
                        artifact = await info.fetchone()
                if artifact[0] == 1:
                    await ctx.send("The Mantle of The Titans glows a dim green... you feel safe. (+50 Defending)")
                    await h.add_effect(ctx.author, self.bot, "defending", amount = 50)
                elif artifact[0] == 2: # Cup of Hell
                    await ctx.send("You drink from the cup of hell... it burns your throat, your stomach... everything! (+666 Coolness | +666 Gold | +666 Burning)")
                    await h.add_coolness(ctx.author.id, 666)
                    await asyncio.sleep(0.2)
                    await h.add_gold(ctx.author.id, 666, self.bot, True)
                    await asyncio.sleep(0.2)
                    await h.add_effect(ctx.author, self.bot, "burning", amount = 666)
        else:
            await ctx.send("You have no artifact.")
    
    @commands.command()
    @commands.guild_only() # Each artifact in game has a unique quest attributed to it. Theses unique quests are coded here.
    async def artifact(self, ctx):
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select artifact from users where id = '{ctx.author.id}';") as info:
                uinfo = await info.fetchone()
        
        aid = uinfo[0]
        
        if aid != "None":
            async with aiosqlite.connect('unique.db') as conn:
                async with conn.execute(f"select * from artifacts where artifact_id = {aid};") as info:
                    artifacts = await info.fetchone()

            embed = discord.Embed(title=f'"{artifacts[2]}"', colour=discord.Colour.from_rgb(218,165,32), description=artifacts[4])
            embed.add_field(name="Lore", value=artifacts[3], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You do not have an artifact.")


async def award_artifact(ctx, uid, aid):
    async with aiosqlite.connect('unique.db') as conn:
        async with conn.execute(f"select * from artifacts where artifact_id = {aid};") as info:
            artifacts = await info.fetchone()

    embed = discord.Embed(title=f'Artifact Unlocked! "{artifacts[2]}"', colour=discord.Colour.from_rgb(218,165,32), description=artifacts[4])
    embed.add_field(name="Lore", value=artifacts[3], inline=False)
    #embed.set_thumbnail(url=quest_info[4])
    async with aiosqlite.connect('unique.db') as conn:
        await conn.execute(f"update artifacts set owner_id = {ctx.author.id} where artifact_id = {aid};")
        await conn.commit()
    async with aiosqlite.connect('main.db') as conn:
        await conn.execute(f"update users set artifact = {aid} where id = '{uid}';")
        await conn.commit()
    await ctx.send(content=ctx.author.mention, embed=embed)

    


# A setup function the every cog has
def setup(bot):
    bot.add_cog(artifacts(bot))
