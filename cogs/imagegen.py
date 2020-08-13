import discord
from discord.ext import commands
import random
import json
import random
import aiohttp
import nekos
import asyncio
import uwuify
import sqlite3 as s
import requests

class Image(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    
    def __embed_json(self, data, key='message'):
        em = discord.Embed(color=0x1B0FDD)
        em.set_image(url=data[key]) 
        return em 
    
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.user)
    async def tweet(self, ctx, username : str, *, text : str):
        await ctx.trigger_typing()
        async with self.session.get('https://nekobot.xyz/api/imagegen?type=tweet'
                                    '&username=%s'
                                    '&text=%s' % (username, text,)) as r:
            res = await r.json()
        await ctx.send(embed=self.__embed_json(res))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def phcomment(self, ctx, *, comment : str):
        if not ctx.message.channel.is_nsfw():
            return await ctx.send('This channel must be marked NSFW to use this command ;)')
        await ctx.trigger_typing()
        async with self.session.get(f'https://nekobot.xyz/api/imagegen?type=phcomment'
                                    f'&image={ctx.author.avatar_url_as(format="png")}'
                                    f'&text={comment}&username={ctx.author.name}') as r:
            res = await r.json()
        if not res["success"]:
            return await ctx.send('**Failed to get image ;-;')
        await ctx.send(embed=self.__embed_json(res))
    

def setup(client):
    client.add_cog(Image(client))