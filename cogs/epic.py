import discord
from discord.ext import commands
import datetime

embed_color = discord.Color(0x2F3136)

class Epic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # basic ping command cause why not lmao
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):

        embed = discord.Embed(title="Pong!", description=f"{round(self.client.latency * 1000)}ms", color=embed_color)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed) # fixed xd

def setup(client):
    client.add_cog(Epic(client))
