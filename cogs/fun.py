import discord
from discord.ext import commands
import requests


@client.command()
async def cat(ctx): 
    url = 'https://some-random-api.ml/img/cat'
    result_url = requests.get(url)
    resultjson=result_url.json()
    embed=discord.Embed(title="here is cat", description="cat", 
    colour=discord.Colour.green())
    embed.set_image(url=resultjson['link'])
    embed.set_footer(text=f"a amazing good cat")      
    await ctx.send(embed=embed)
    
@client.command()   
async def dog(ctx): 
    url = 'https://some-random-api.ml/img/dog'
    result_url = requests.get(url)
    resultjson=result_url.json()
    embed=discord.Embed(title="here is dog", description="dog", 
    colour=discord.Colour.green())
    embed.set_image(url=resultjson['link'])
    embed.set_footer(text=f"a amazing good dog")      
    await ctx.send(embed=embed)
    
@client.command()
async def meme(ctx):
    url = 'https://some-random-api.ml/meme'
    result_url = requests.get(url)
    resultjson=result_url.json()
    embed=discord.Embed(title=resultjson['caption'], colour=discord.Colour.purple())
    embed.set_image(url=resultjson['image'])
    embed.set_footer(text=f"Category: {resultjson[ 'category']}")
    await ctx.send(embed=embed)
