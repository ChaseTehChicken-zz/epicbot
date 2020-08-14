import discord
from discord.ext import commands
import datetime
import random


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

    # get a random kaomoji bear
    @commands.command()
    @commands.cooldown(1,2, commands.BucketType.user)
    async def bear(self, ctx):
        bears = ["ʕ •ᴥ•ʔ", "ᶘ ᵒᴥᵒᶅ", "ᶘ ⊙ᴥ⊙ᶅ", "ᶘ °㉨°ᶅ", "ᶘಠᴥಠᶅ", "ʕ •́؈•̀)", "ʕ´ڡ｀*ʔ", "ʕ – _ – ʔ", "ʕ – o – ʔ", "（´•(ｪ)•｀）", "ʕ≧(ｴ)≦ ʔ",
                "ʕ •㉨• ʔ", "ʕó㉨òʔﾉ♡", "ᶘ ᵒ㉨ᵒᶅ", "ʕ´•㉨•`ʔ", "ʕ≧㉨≦ʔ", "ʕ✪㉨✪ʔ", "ʕ ̿–㉨ ̿– ʔ", "ʕ/　·ᴥ·ʔ/", "ʕ； •`ᴥ•´ʔ", "ʕ ˵• ₒ •˵ ʔ",
                "ʕ •ᴥ•ʔゝ☆", "ᕕʕ •ₒ• ʔ୨", "ʕ　·ᴥʔ", "ʕ·ᴥ·　ʔ", "ʕᴥ·　ʔ", "ʕ •ᴥ•ʔ", "ʕง•ᴥ•ʔง"]
        await ctx.send(" " + random.choice(bears))

def setup(client):

    client.add_cog(Epic(client))