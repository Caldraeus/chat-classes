import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import aiosqlite
import asyncio
import random
from discord import Webhook, AsyncWebhookAdapter
import aiohttp


base_classes = {
    1 : 'Apprentice',
    2 : 'Swordsman',
    3 : 'Rogue',
    4 : 'Archer',
}

prefix = ';'

with open('adjectives.txt') as f:
    sheep_names = [line.rstrip() for line in f]

body_parts = ['bones', 'hair', 'fingernail', 'thumb', 'middle finger', 'big toe', 'knees', 'kneecap', 'bum', 'cheek', 'bumcheek', 'leg hair', 'skeleton', 'ligaments', 'muscles', 'tendons', 'teeth', 'mouth', 'tongue', 'larynx', 'esophagus', 'stomach', 'small intestine', 'large intestine', 'liver', 'gallbladder', 'mesentery', 'pancreas', 'anus', 'nasal cavity', 'pharynx', 'larynx', 'trachea', 'lungs', 'diaphragm', 'groin', 'kidneys', 'heart', 'spleen', 'thymus', 'brain', 'cerebellum', 'spine', 'eye', 'ear', 'arm', 'leg', 'chest', 'neck', 'toe', 'finger']

async def add_effect(target, bot, effect_name, amount = 1):
    speaker = target.id
    if speaker not in bot.user_status:
        bot.user_status[speaker] = []
    user_effects = bot.user_status[speaker]
    exists = False
    for status in user_effects: # If the status exists, increment it.
        if status[0].lower() == effect_name.lower():
            exists = True
            status[1] += amount
    if not exists:
        bot.user_status[speaker].append([effect_name.lower(), amount])


effect_list = {
    "shatter" : "Your mind has been shattered! Your messages are jumbled up!",
    "polymorph" : "You're a sheep! You can't speak human languages!"
}
async def handle_effects(message, bot): # List of effects in the readme
    speaker = message.author.id
    if speaker in bot.user_status:
        user_effects = bot.user_status[speaker]
        for status in user_effects: # We go through each status affecting the user [NOT ALL APPLY TO ON-MESSAGE EVENTS. THEREFORE, WE NEED IF STATEMENTS]. These are applied in order
            if status[0].lower() == "shatter":
                ### HANDLE STACKS
                remaining_stacks = status[1]-1
                if remaining_stacks <= 0:
                    bot.user_status[speaker].remove(status)
                else:
                    status[1] -= 1
                ### APPLY EFFECT
                while True:
                    mad_content = " "
                    content = message.content.split(" ")
                    random.shuffle(content)
                    mad_content = mad_content.join(content)
                    if mad_content != message.content or all(x==content[0] for x in content) == True:
                        break
                
                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await webhook_safe_check(message.channel)
                    clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    await clone_hook.send(content=mad_content, username=message.author.display_name, avatar_url=message.author.avatar_url)
            elif status[0].lower() == "polymorph":
                ### HANDLE STACKS
                remaining_stacks = status[1]-1
                if remaining_stacks <= 0:
                    bot.user_status[speaker].remove(status)
                else:
                    status[1] -= 1
                ### APPLY EFFECT
                
                urls = [
                    "https://assets-global.website-files.com/5bbd49a137709a4145049ab0/5dd67614e984aa331e6dc8be_Fronde--blog-hero-image_0001_sheep.jpg",
                    "https://thumbs-prod.si-cdn.com/SkuS5xz-Q-kr_-ol6xblY9fsoeA=/fit-in/1600x0/https://public-media.si-cdn.com/filer/d4/f6/d4f6e4bf-8f77-445d-a8f9-e3a74c6a40f0/ewkhdqqwsae0xpo.jpeg",
                    "https://i.guim.co.uk/img/media/22bed68981e92d7a9ff204ed7d7f5776a16468fe/1933_1513_3623_2173/master/3623.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=b7545d644ba9f6bcc673a8bdf6d7db83",
                    "https://images.theconversation.com/files/324133/original/file-20200330-173620-1q1nz5d.jpg?ixlib=rb-1.1.0&rect=0%2C697%2C4635%2C2314&q=45&auto=format&w=1356&h=668&fit=crop",
                    "https://viva.org.uk/wp-content/uploads/2020/05/fun-facts.jpg",
                    "https://spca.bc.ca/wp-content/uploads/lamb-in-grassy-field-825x550.jpg",
                    "https://s7657.pcdn.co/wp-content/uploads/2016/01/Fluffy-sheep-940x480.jpg",
                    "https://www.macmillandictionary.com/external/slideshow/thumb/137411_thumb.jpg",
                    "https://www.abc.net.au/cm/rimage/9673494-3x4-xlarge.jpg?v=3",
                    "https://ichef.bbci.co.uk/news/1024/cpsprodpb/081B/production/_98657020_c0042087-black_faced_sheep-spl.jpg"
                ]

                random.seed(len(message.content))
                sheep_content = ""
                for word in message.content.split(" "):
                    if word[-1] == ".":
                        sheep_content += f"b{random.randint(1,10)*'a'}. "
                    elif word[-1] == "!":
                        sheep_content += f"b{random.randint(1,10)*'a'}! "
                    elif word[-1] == ":":
                        sheep_content += f"b{random.randint(1,10)*'a'}: "
                    elif word[-1] == "?":
                        sheep_content += f"b{random.randint(1,10)*'a'}? "
                    elif word[-1] == ",":
                        sheep_content += f"b{random.randint(1,10)*'a'}, "
                    else:
                        sheep_content += f"b{random.randint(1,10)*'a'} "

                random.seed(message.author.id)
                sheep_name = random.choice(sheep_names).title() + " Sheep"
                chosen_url = random.choice(urls)

                await message.delete()
                async with aiohttp.ClientSession() as session:
                    url = await webhook_safe_check(message.channel)
                    clone_hook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
                    
                    try:
                        await clone_hook.send(content=sheep_content.capitalize(), username=sheep_name, avatar_url=chosen_url)
                    except:
                        await clone_hook.send(content="Ba"*random.randint(1,20), username=sheep_name, avatar_url=chosen_url)



async def can_attack(user, target, ctx): # NOTE: Remember that you can't alter AP of those who have no profile in CC...
    return True

def max_xp(lvl):
    return 15 * (lvl ^ 15) + 150 * lvl + 15

async def alter_items(uid, ctx, bot, item, change = 1, cost = 0):
    item = item.lower()
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select inventory, gold from users where id = '{uid}'") as u_info:
            user_info = await u_info.fetchone()

    inv = user_info[0].split("|")
    gold = user_info[1]
    
    for owned_item in inv:
        new_guy = owned_item.split(",")
        inv[inv.index(owned_item)] = new_guy

    items = [item[0] for item in inv] # Array of just the names of the items in the 2D array.
    end = ""

    if gold - cost < 0:
        await ctx.send("You cannot afford this item!")
    else:
        if item in items:
            index = items.index(item)
            item_amount = int(inv[index][1]) + change
            inv[index][1] = str(item_amount)
            if item_amount >= 10:
                await award_ach(14, ctx.message, bot)

        for sublist in inv:
            if inv.index(sublist) == len(inv)-1:
                end += f"{','.join(sublist)}"
            else:
                end += f"{','.join(sublist)}|"
        
        if item not in items:
            end+=f"|{item},{change}"
            
        async with aiosqlite.connect('main.db') as conn:
            await conn.execute(f"update users set gold = {gold - cost}, inventory = '{end}' where id = '{uid}';")
            await conn.commit()
        if cost > 0:
            await ctx.send(f"✅ | Purchase complete! Your gold balance is now {gold-cost}.")

async def alter_ap(message, ap, bot):
    if str(message.author.id) in bot.registered_users:
        uid = str(message.author.id)
        balance = (bot.users_ap[uid] - ap)
        if balance >= 0:
            bot.users_ap[uid] = balance
            return True
        else:
            await message.channel.send("You don't have enough AP to do that! Buy some refreshers from the shop, do some quests, or wait until rollover!")
            return False

async def xp_handler(message, bot):
    testing = True
    num = random.randint(1,4)
    if num == 4:
        if str(message.author.id) in bot.registered_users:
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select exp, level from users where id = '{message.author.id}';") as profile:
                    prof = await profile.fetchone()
            xp = prof[0] + random.randint(5,50)
            current_lvl = prof[1]
            if xp >= max_xp(current_lvl) and ((prof[1]+1) % 10 != 0):
                async with aiosqlite.connect('main.db') as conn:
                    await conn.execute(f"update users set exp = 0 where id = '{message.author.id}'")
                    await conn.execute(f"update users set level = {current_lvl + 1} where id = '{message.author.id}'")
                    await conn.commit()
                embed = discord.Embed(title=f"✨ Level up! ✨", colour=discord.Colour.from_rgb(255, 204, 153), description=f'You are now level {prof[1]+1}! Good job!')
                embed.set_thumbnail(url=message.author.avatar_url)
                notif = await message.channel.send(content=message.author.mention, embed=embed)
                await notif.delete(delay=10)
            elif xp >= max_xp(current_lvl) and ((prof[1]+1) % 10 == 0):
                async with aiosqlite.connect('main.db') as conn:
                    await conn.execute(f"update users set exp = {max_xp(current_lvl)} where id = '{message.author.id}'")
                    await conn.commit()
                if message.author.id not in bot.notified and not testing:
                    bot.notified.append(message.author.id)
                    embed = discord.Embed(title=f"✨ Level up! ✨", colour=discord.Colour.from_rgb(255, 204, 153), description=f'You can now level up to {prof[1]+1}! Good job!')
                    embed.set_thumbnail(url=message.author.avatar_url)
                    embed.set_footer(text=f"A class up is available! Run {prefix}classup when you are ready.", icon_url="https://lh3.googleusercontent.com/proxy/KbtIDDPpLGgzz6LmKyMoyYRtnXpgPHjyvr3Idg30Cff8JDcfXTiVdjl9QjGn_G_ty6ekXk29X2BwNJ8mdz-QfIHhMs7qd7HA")
                    notif = await message.channel.send(content=f'{message.author.mention}', embed=embed)
                    await notif.delete(delay=10)
                
            else:
                async with aiosqlite.connect('main.db') as conn:
                    await conn.execute(f"update users set exp = {xp} where id = '{message.author.id}'")
                    await conn.commit()
                    

async def webhook_safe_check(channel): # This function should be run before any webhook command in main.py. It makes sure that the channel has a webhook, and if it doesn't, it creates one.
    seeking_id = channel.id
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select * from webhooks where channel_id = '{seeking_id}';") as chan:
            hook = await chan.fetchone()
        if hook:
            return hook[1]
        else:
            new_hook = await channel.create_webhook(name=f"Chat Classes {channel.name} Webhook")
            await conn.execute(f"insert into webhooks values('{channel.id}', '{new_hook.url}')")
            await conn.commit()
            return new_hook.url

basic_text_quests = [1,2,3,4,5,6]
async def on_message_quest_handler(user, mss, people): # This takes the message sent, checks if it's applicable to any quest. I just put it here instead of main.py honestly.
    uid = str(user.id)
    if uid in people:
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select completed_quests, currently_questing from users where id = '{uid}';") as chan:
                quest = await chan.fetchone()
        if quest:
            if quest[1] != 0: # If the user has a quest...
                if quest[1] in basic_text_quests:
                    await update_quest(mss, quest[1], 1)

async def update_quest(message, quest_id, addition):
    if addition > 0: # Setting addition to 0 will fail their quest.
        chan = message.channel
        user = message.author
        notif = None # To prevent locked db errors.
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select * from quests where quest_id = {quest_id}") as q_info:
                quest_info = await q_info.fetchone()

        questers = quest_info[5].split("|")

        for guy in questers:
            new_guy = guy.split(",")
            questers[questers.index(guy)] = new_guy # I don't want to comment this and I know I will regret this. 
            # print(f"I am setting {new_guy} up to replace {guy}.")

        found = False
        for new_guy in questers: # Have to do this in a seperate loop to prevent a critical error.
            if new_guy[0] == str(user.id):
                found = True
                new_guy[1] = str(int(new_guy[1]) + addition)
                
                if int(new_guy[1]) >= int(quest_info[7]):
                    questers.pop(questers.index(new_guy))
                    async with aiosqlite.connect('main.db') as conn:
                        async with conn.execute(f"select completed_quests from users where id = '{message.author.id}'") as count:
                            old_count = await count.fetchone()
                            new_count = old_count[0] + 1
                        await conn.execute(f"update users set completed_quests = {new_count} where id = '{message.author.id}';")
                        await conn.commit()
                    async with aiosqlite.connect('main.db') as conn:
                        if quest_info[2] == "coolness": # REWARD TYPES!
                            async with conn.execute(f"select coolness from users where id = '{message.author.id}'") as coolness:
                                old_cool = await coolness.fetchone()
                                new_cool = old_cool[0] + int(quest_info[3])
                                await conn.execute(f"update users set coolness = {new_cool} where id = '{message.author.id}';")
                                await conn.commit() 
                                reward = f"+{quest_info[3]} Coolness"
                        elif quest_info[2] == "xp": 
                            async with conn.execute(f"select exp from users where id = '{message.author.id}'") as exp:
                                old_exp = await exp.fetchone()
                                new_exp = old_exp[0] + int(quest_info[3])
                                await conn.execute(f"update users set exp = {new_exp} where id = '{message.author.id}';")
                                await conn.commit() 
                                reward = f"+{quest_info[3]} XP"
                        elif quest_info[2] == "gold": 
                            async with conn.execute(f"select gold from users where id = '{message.author.id}'") as exp:
                                old_cash = await exp.fetchone()
                                new_cash = old_cash[0] + int(quest_info[3])
                                await conn.execute(f"update users set gold = {new_cash} where id = '{message.author.id}';")
                                await conn.commit() 
                                reward = f"+{quest_info[3]} Gold"
                        else:
                            pass

                        await conn.execute(f"update users set currently_questing = 0 where id = '{message.author.id}';")
                        await conn.commit()

                    embed = discord.Embed(title=f"Quest Complete!", colour=discord.Colour.from_rgb(166, 148, 255), description=f'**{quest_info[6]}**\n*{quest_info[1]}*')
                    embed.set_footer(text=reward, icon_url="")
                    embed.set_thumbnail(url=quest_info[4])
                    notif = await chan.send(content=message.author.mention, embed=embed)
            if notif:
                await notif.delete(delay=10)

            end = ""
            for sublist in questers:
                if questers.index(sublist) == len(questers)-1:
                    end += f"{','.join(sublist)}"
                else:
                    end += f"{','.join(sublist)}|"

            async with aiosqlite.connect('main.db') as conn:
                await conn.execute(f"update quests set users = '{end}' where quest_id = '{quest_id}';")
                await conn.commit()

        if found == False:
            print("Locked. Probably.")
            for i in range(0,50): # Try only 50 times.
                while True:
                    try:
                        async with aiosqlite.connect('main.db') as conn:
                            await conn.execute(f"update users set currently_questing = 0 where id = '{message.author.id}';")
                            await conn.commit()
                    except ValueError:
                        continue
                    break
    else:
        pass # For failing quests. Not yet implemented.
                        
                



###################################################################
###################################################################
################## ACHIEVEMENT HANDLING ###########################
###################################################################
###################################################################

necromancer_triggers = [
    "i want to die",
    "i died",
    "i am dead",
    "i am dying",
    "i am going to die",
    "i dieded",
    "want to be a necromancer",
    "wish i was a necromancer"
]

old_bot_triggers = [
    "robo head",
    "asami",
    "skeletor",
    "robo_head",
    "runebot",
    "rune bot",
    "waifu battles"
]

janitor_triggers = [
    "frick",
    "heck",
    "darn",
    "h*ck",
]


async def txt_achievement_handler(content, uid, message_obj, bot): # This is going to be a long mess... This is the handler for text-based achievements ONLY! 
    unlocked = bot.registered_users[str(uid)]
    ach_id = 0
    if any(trg in content for trg in necromancer_triggers) and 1 not in unlocked:
        ach_id = 1
    elif "@everyone" in content and 2 not in unlocked:
        ach_id = 2
    elif "a" in content and content != f"{prefix}start" and 3 not in unlocked:
        ach_id = 3
    elif "<@!713506775424565370>" in content or "<@713506775424565370>" in content and 4 not in unlocked:
        ach_id = 4
    elif message_obj.guild.id == 732632186204979281 and 5 not in unlocked:
        ach_id = 5
    elif content == "<@!217288785803608074>" or content == "<@217288785803608074>" and 6 not in unlocked:
        ach_id = 6
    elif any(trg in content for trg in old_bot_triggers) and 7 not in unlocked:
        ach_id = 7
    elif any(trg in content for trg in janitor_triggers) and 8 not in unlocked:
        ach_id = 8
    elif "no tomb can hold me" in content and 10 not in unlocked:
        ach_id = 10
    elif "groovy" in content and 11 not in unlocked:
        ach_id = 11

    # Above determines which achievement has been obtained. Below takes that id and sends the embed as well as awarding the achievement.
    
    if ach_id != 0 and ach_id not in unlocked:
        await award_ach(ach_id, message_obj, bot)


async def add_coolness(uid, amount):
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select coolness from users where id = '{uid}';") as current_amount:
            coolness = await current_amount.fetchone()
            await conn.execute(f"update users set coolness = '{coolness[0]+amount}' where id = '{uid}';")
            await conn.commit()

async def add_gold(uid, amount, bot):
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute(f"select gold from users where id = '{uid}';") as current_amount:
            gold = await current_amount.fetchone()
            if uid in bot.server_boosters and amount > 0:
                amount *= 2
            final = gold[0]+amount
            if final < 0:
                final = 0
            await conn.execute(f"update users set gold = '{final}' where id = '{uid}';")
            await conn.commit()

async def award_ach(ach_id, message, bot):
    uid = message.author.id
    unlocked = bot.registered_users[str(uid)]
    if ach_id not in unlocked:
        async with aiosqlite.connect('main.db') as conn:
            async with conn.execute(f"select achievements from users where id = '{uid}';") as person:
                user_ach = await person.fetchone() # While these lines are repeats from the txt_achievement_handler, this function can be used in other lines of code to award achievements, so this unfortunate redundancy has to stay for now.
                user_ach = user_ach[0].split("|")
                user_ach.append(str(ach_id))
                user_ach = '|'.join(user_ach)
                await conn.execute(f"update users set achievements = '{user_ach}' where id = '{uid}'")
                await conn.commit()
        
            async with conn.execute(f"select * from achievements where id = '{ach_id}'") as ach:
                ach_info = await ach.fetchone()
                embed = discord.Embed(title=f"Achievement Unlocked!", colour=discord.Colour.from_rgb(255,200,0), description=f'**"{ach_info[1]}"**\n*{ach_info[2]}*')
                embed.set_thumbnail(url=ach_info[3])
                amount = ach_info[4]
                embed.set_footer(text=f"+{amount} Coolness", icon_url="")
                # await asyncio.sleep(random.randint(30,100))
            async with conn.execute(f"select coolness from users where id = '{uid}';") as current_amount: # Can't run the function for this due to overloading the db
                coolness = await current_amount.fetchone()
                await conn.execute(f"update users set coolness = '{coolness[0]+amount}' where id = '{uid}';")
                await conn.commit()
            async with conn.execute(f"select id, achievements from users;") as people:
                usrs = await people.fetchall()
                for guy in usrs: # Regenerate the list of people with achievements.
                    user_ach = guy[1].split("|")
                    unlocked = []
                    for stringnum in user_ach: # Just for the if statement. I really hate this and want to fix it eventually.
                        unlocked.append(int(stringnum))
                        
                        bot.registered_users[guy[0]] = unlocked

            mss = await message.channel.send(content=message.author.mention, embed=embed)
            await mss.delete(delay=10)
            


async def fetch_random_quest(message, bot, uid=None, override=False):
    # Random quest encounter chance time!
    if uid:
        uid = str(uid)
    else:
        uid = str(message.author.id)
    if uid in bot.registered_users:
        chance = random.randint(1,100)
        if override:
            chance = 52
        if chance == 52: 
            async with aiosqlite.connect('main.db') as conn:
                async with conn.execute(f"select currently_questing from users where id = '{uid}';") as people:
                    usrs = await people.fetchall()
                    if usrs != []:
                        if usrs[0][0] == 0: # If they don't have a quest...
                            async with conn.execute("select count(*) from quests;") as numcount:
                                num = await numcount.fetchone()
                                total_quests = num[0]
                            chosen_quest = random.randint(1, total_quests)
                            async with conn.execute(f"select * from quests where quest_id = {chosen_quest}") as q_info: # Why not select just the users? In case I want to do something with the quest info later. Futureproofing, I suppose.
                                quest_info = await q_info.fetchone()
                                questers = quest_info[5]
                            questers += f"{uid},0|"
                            await conn.execute(f"update quests set users = '{questers}' where quest_id = {chosen_quest};")
                            await conn.execute(f"update users set currently_questing = {chosen_quest} where id = '{uid}';")
                            await conn.commit()
                            embed = discord.Embed(title=f"New Quest!", colour=discord.Colour.from_rgb(255,200,0), description=f"**{quest_info[6]}**\n*{quest_info[1]}*") 
                            embed.set_thumbnail(url=quest_info[4])
                            embed.set_footer(text=f"Reward: {quest_info[2].title()} ({quest_info[3]})", icon_url="")
                            notif = await message.channel.send(content=message.author.mention, embed=embed)
                            await notif.delete(delay=5)

#########################################################
#########################################################
#########################################################
#########################################################
#########################################################

async def genprof(uid, aps):
    async with aiosqlite.connect('main.db') as conn:
        async with conn.execute("select count(*) from achievements;") as numcount:
            num = await numcount.fetchone()
            total_achievements = num[0] # Self explanatory.
        async with conn.execute(f"select * from users where id = '{uid.id}';") as info:
            user = await info.fetchone()

    profile = discord.Embed(title=f"{uid.display_name}'s Profile", colour=discord.Colour(0x6eaf0b), description="")
    profile.set_thumbnail(url=uid.avatar_url)
    ###
    user_ach = user[6].split("|")
    user_ach = len(user_ach)-1
    clss = user[1].replace("_"," ")
    clss = clss.title()
    ###
    profile.set_footer(text=f"Global Coolness Ranking: {await genrank(uid.id)}", icon_url="")
    profile.add_field(name="Class & Level", value=f'{user[1].title()} ║ Level {user[8]}', inline=False)
    profile.add_field(name="Coolness", value=user[5])
    profile.add_field(name="Gold", value=user[3])
    profile.add_field(name="Achievements", value=f"{user_ach} of {total_achievements} Unlocked ({int((user_ach/total_achievements)*100)}%)", inline=False)
    profile.add_field(name="Experience", value=f"{user[2]} / {max_xp(user[8])} ({int((user[2]/max_xp(user[8]))*100)}%)", inline=False)
    profile.add_field(name="Completed Quests", value=user[9], inline=False)
    profile.add_field(name="Action Points", value=aps[str(uid.id)], inline=False)
    # profile.add_field(name=) Put equipment here eventually
    
    return(profile)

async def genrank(uid):
    async with aiosqlite.connect('main.db') as con:
        async with con.execute(f"select * from users order by coolness desc;") as lb: # Get their coolness rank!
            stuff = await lb.fetchall()
            rank = 1
            for usr in stuff:
                if usr[0] == str(uid):
                    break
                else:
                    rank+=1
            return(rank)