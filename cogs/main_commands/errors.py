import traceback
import sys
from discord.ext import commands
import discord
import sqlite3


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'): 
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, sqlite3.OperationalError):
            print(f"Databse locked error:\n\n{error}\n\n")
            return
        
        elif isinstance(error, discord.ext.commands.errors.NotOwner):
            return await ctx.send("Hate to rain on your parade, pal, but that's a me-only command.")

        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            return
        
        # elif isinstance(error, KeyError):
        #     return await ctx.send('🚫 | You are not that class, or you have no profile! Run `;class` to see your commands!')

        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You do not have permission to run this command!")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'Commands are disabled in Private Messages.')
            except:
                pass

        elif isinstance(error, commands.CommandOnCooldown):
            mss = await ctx.send(f"{ctx.author.mention} : Slow down, hotshot! Command is on cooldown!")
            await mss.delete(delay=5)

        if not isinstance(error, commands.CommandOnCooldown):
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
                

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))


"""

0,0|260512821819736066,463|278534820760518656,184|309104167052640257,392|742892694375891044,288|469182909501276160,5|712302942035640360,252|522901677234454546,183|296741861198921731,250|
"""