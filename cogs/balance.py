import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import datetime

db_name = cluster["Discord"]
balance = db_name["Balance_Setup"]
exists = cluster.list_database_names()

class Balance(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["createbal", "cb"])
    @commands.cooldown(1,10, commands.BucketType.user)
    async def createbalance(self, ctx):
        try:
            create_account = {
                "_id": ctx.author.id,
                "balance": 0,
                "rob mode": "Off"
            }
            balance.insert_one(create_account)
            find_bal = balance.insert_one({"_id": ctx.author.id})
            embed = discord.Embed(title="Balance", description="{}'s balance: ${}".format(ctx.author.mention, find_bal["balance"]), color=0x1B0FDD)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        except pymongo.errors.DuplicateKeyError as exc:
            print(exc)
            embed = discord.Embed(title="Error", description="Something went wrong! Most likely your account exists already!", color=0x1B0FDD)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Balance(client))
