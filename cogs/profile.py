import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import datetime
import asyncio

cluster = MongoClient("DM Purple Guy#1234 for Mongo URL")
db = cluster["Discord"]
pro = db["Profile"]

class Profile(commands.Cog):

    def __init__(self, client):

        self.client = client
    
    # Profile command
    # Usage: >>profile
    # Notes: It will prompt you so it doesn't require any args.
    @commands.command()
    @commands.cooldown(1,30, commands.BucketType.user)
    async def addprofile(self, ctx):
        try:
            try:
                await ctx.send("**What is your name (doesn't have to be your real name)**")

                # checking
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel and message.content == message.content

                # res 1
                name = await self.client.wait_for('message', check=check, timeout=60)
                await ctx.send("**What is your gender?**")

                # checking
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel and message.content == message.content
                
                # res 2
                gen = await self.client.wait_for('message', check=check, timeout=60)
                await ctx.send("**Tell us about yourself**")

                # checking
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel and message.content == message.content

                # res 3
                hobs = await self.client.wait_for('message', check=check, timeout=60)
                await ctx.send("**What do you like?**")

                # checking
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel and message.content == message.content

                #res 4
                dis = await self.client.wait_for('message', check=check, timeout=60)
                await ctx.send("**What do you dislike?**")

                # checking
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel and message.content == message.content

                # res 5
                end = await self.client.wait_for('message', check=check, timeout=60)
                m = await ctx.send("**Creating your profile, please wait..**")
                upd = True

                while upd == True:
                    await m.edit(content="**Creating your profile, please wait...**")
                    await asyncio.sleep(3)
                    await m.edit(content="**Creating your profile, please wait..**")
                    await asyncio.sleep(3)
                    await m.edit(content="**Creating your profile, please wait.**")
                    await asyncio.sleep(3)
                    await m.edit(content="**Creating your profile, please wait...**")
                    await asyncio.sleep(3)
                    await m.edit(content="**Creating your profile, please wait..**")
                    await asyncio.sleep(3)
                    await m.edit(content="**Creating your profile, please wait.**")
                    await m.delete()
                    upd = False
                
                make_db = {
                    "_id": ctx.author.id,
                    "Name": name.content,
                    "Gender": gen.content,
                    "Info": hobs.content,
                    "Likes": dis.content,
                    "Dislikes": end.content,
                }
                pro.insert_one(make_db)

                await ctx.send("**{}, your profile is created!**".format(ctx.author.mention))    


            except Exception as exc:
                if pymongo.errors.DuplicateKeyError:
                    await ctx.send("**{}, seems like your profile already exists! If you'd like to reset your profile please run `>>delprofile`**".format(ctx.author.mention))
                else:
                    await ctx.send("**Something went wrong..**")
        except asyncio.TimeoutError:
            await ctx.send("**Too slow! Prompt ended, {}!**".format(ctx.author.mention))

    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.user)
    async def delprofile(self, ctx):
        pro.delete_one({"_id": ctx.author.id})
        await ctx.send("**{} your profile stats have been reset, you may run `>>addprofile` to create a profile!**".format(ctx.author.mention))

    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.user)
    async def profile(self, ctx):
        try:
            find = pro.find_one({"_id": ctx.author.id})
            em = discord.Embed(colour=discord.Colour.orange())
            em.timestamp = datetime.datetime.utcnow()
            em.add_field(name="**Name**", value=find["Name"])
            em.add_field(name="**Gender**", value=find["Gender"])
            em.add_field(name="**Description**", value=find["Info"])
            em.add_field(name="**Likes**", value=find["Likes"])
            em.add_field(name="**Dislikes**", value=find["Dislikes"])
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            em.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send("**Could not find your profile, please run `>>addprofile` to make one!**")


def setup(client):
    client.add_cog(Profile(client))
