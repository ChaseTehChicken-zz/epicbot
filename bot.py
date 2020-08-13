import discord
import os
import json
import sqlite3
import pymongo
from pymongo import MongoClient
from discord.ext import commands

dev_ids = [188728919774461952, 514858928983506959, 420454043593342977]

client = commands.Bot(command_prefix=commands.when_mentioned_or(">>"))
client.remove_command('help')

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user.name}\nID: {client.user.id}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token) # make token variable
