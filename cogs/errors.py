import discord
from discord.ext import commands
import datetime
import sys
import traceback

class Error(commands.Cog):

    def __init__(self, client):

        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        error = getattr(exception, "original", exception)
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Slow Down Buddy!", description=f"You may retry in {round(error.retry_after)}s", color=0x2f3136)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        elif isinstance(error, discord.NotFound):
            return
        elif isinstance(exception, commands.BadArgument):
            return
        elif isinstance(exception, commands.CommandNotFound):
            return
        elif isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send('Command is missing required argument!')
        elif isinstance(exception, commands.MissingPermissions):
            embed = discord.Embed(description='You are missing the correct permissions to run this command!', color=0x2f3136)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            raise error
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



def setup(client):

    client.add_cog(Error(client))