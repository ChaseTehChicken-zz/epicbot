import discord
from discord.ext import commands
import datetime


class Epic(commands.Cog):

    def __init__(self, client):

        self.client = client

    # basic ping command cause why not lmao
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.user)
    async def ping(self, ctx):

        embed = discord.Embed(title="Pong!", description=f"{round(self.client.latency * 1000)} MS", color=0x2f3136)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed) # fixed xd

def setup(client):

    client.add_cog(Epic(client))