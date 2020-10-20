import discord
from discord.ext import commands
import helper as h
from discord.ext.commands.cooldowns import BucketType
import random
import math
import os
import aiohttp
import aiosqlite
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

class help_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    pass

    @commands.command()
    @commands.guild_only()
    async def server(self, ctx):
        await ctx.send("Join the official server here!\n\nhttps://discord.gg/JRxUGCA")

    @commands.command()
    @commands.guild_only()
    async def roadmap(self, ctx):
        embed = discord.Embed(title="", colour=discord.Colour(0x2dc3e1), description="")

        embed.set_image(url="https://cdn.discordapp.com/attachments/734108098129821757/736602739190267934/unknown.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.guild_only()
    async def help(self, ctx, module = "modules"):
        pages = 1
        module = module.lower()
        profile = discord.Embed(title=f"Chat Classes Help", colour=discord.Colour.from_rgb(128, 128, 128), description="")
        profile.set_footer(text=f"Use {h.prefix}help module to see specific commands!", icon_url="")
        if module == "modules":
            profile.add_field(name="Profile", value='View commands related to your profile.', inline=False)
            profile.add_field(name="General", value="View general commands.", inline=False)
            profile.add_field(name="Server", value="View server management commands.", inline=False)
            profile.add_field(name="Class", value="View class commands.", inline=False)
            profile.add_field(name="Shop", value="View shop commands.", inline=False)
            profile.set_thumbnail(url="https://archive-media-0.nyafuu.org/c/image/1531/86/1531863615508.png")
            await ctx.send(embed=profile)
        elif module == "profile":
            profile.add_field(name="profile {optional: @user}", value="Display someones profile.", inline=False)
            profile.add_field(name="achs {optional: @user}", value="Display someones achievements.", inline=False)
            profile.add_field(name="quest", value="Show your current quest, if you have one.", inline=False)
            profile.add_field(name="classup", value="Choose your next class. Only works if you're a level below a level equal to a multiple of ten and have 100% xp. (10, 20, 30...)", inline=False)
            profile.set_thumbnail(url="https://archive-media-0.nyafuu.org/c/image/1531/86/1531863615508.png")
            await ctx.send(embed=profile)
        elif module == "general":
            profile.add_field(name="top", value="Display the global top 5 users based on coolness.", inline=False)
            profile.add_field(name="about", value="Display bot information.", inline=False)
            profile.add_field(name="invite", value="Send the bots invite link.", inline=False)
            profile.add_field(name="help", value="Display the help embed.", inline=False)
            profile.add_field(name="server", value="Send the official Chat Classes server invite.", inline=False)
            profile.add_field(name="roadmap", value="View the current Chat Classes roadmap.", inline=False)
            profile.set_thumbnail(url="https://archive-media-0.nyafuu.org/c/image/1531/86/1531863615508.png")
            await ctx.send(embed=profile)
        elif module == "server":
            profile.add_field(name="safezone", value="Disable bot from running in a channel.", inline=False)
            profile.add_field(name="classzone", value="Enable the bot to run in a channel. This is enabled by default.", inline=False)
            profile.add_field(name="enablecc", value="Enable the bot for your server.", inline=False)
            profile.add_field(name="disclaimer", value="Display the disclaimer message.", inline=False)
            profile.set_thumbnail(url="https://archive-media-0.nyafuu.org/c/image/1531/86/1531863615508.png")
            await ctx.send(embed=profile)
        elif module == "class":
            profile.add_field(name="start", value="Register with the bot to begin using class commands.", inline=False)
            profile.add_field(name="classinfo", value="Show your class specific commands.", inline=False)
            profile.set_thumbnail(url="https://archive-media-0.nyafuu.org/c/image/1531/86/1531863615508.png")
            await ctx.send(embed=profile)
        elif module == "shop":
            profile.add_field(name=f"shop [type] [page]", value="Check the shop for a specific item type. Saying just `{h.prefix}shop` is the same as saying `{prefix}shop consumables 1`.", inline=False)
            profile.add_field(name="inventory", value="Display your item inventory.", inline=False)
            profile.add_field(name="use [item]", value="Use an item.", inline=False)
            profile.set_thumbnail(url="https://archive-media-0.nyafuu.org/c/image/1531/86/1531863615508.png")
            await ctx.send(embed=profile)
    
            


# A setup function the every cog has
def setup(bot):
    bot.add_cog(help_commands(bot))
