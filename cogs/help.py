import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def help(self, ctx, args=None):
        if args == None:
            e = discord.Embed(title='Epic Help Command!', color=0xfa00e9)
            e.add_field(name='>>help imagegen', value='Image generation commands')
            e.add_field(name='>>help mod', value='Epic Moderation commands')
            e.add_field(name='>>help fun', value='Epic F.U.N. stuff')
            e.add_field(name='>>help misc', value='Miscellaneous things (they often get lonely)')
            await ctx.send(embed=e)
        if args == 'fun':
            e = discord.Embed(title='Super F.U.N. commands')
            e.add_field(name='>>kaomoji_bear', value='Sends a random bear kaomoji')
            e.add_field(name='>>kaomoji_positive', value='Sends a random happy kaomoji')
            e.add_field(name='>>kaomoji_negative', value='Sends a random sad kaomoji')
            e.add_field(name='>>kaomoji_neutral', value='Sends a random neutral kaomoji')
            e.add_field(name='>>cat', value='Generate an image of a cat')
            e.add_field(name='>>dog', value='Generate an image of a dog')
            e.add_field(name='>>panda', value='Generate an image of a panda')
            e.add_field(name='>>redpanda', value='Generate an image of a redpanda')
            e.add_field(name='>>birb', value='Generate an image of a birb')
            e.add_field(name='>>fox', value='Generate an image of a fox')
            e.add_field(name='>>koala', value='Generate an image of a koala')
            e.add_field(name='>>meme', value='Get a haha funny me me')
            e.add_field(name='>>char (sentence/word)', value='Get the amount of characters in a sentence')
            e.add_field(name='>>google/lmgtfy (query)', value='Let Me Google That For You')
            e.add_field(name='>>clap/sassify/sass (sentence/word)', value='Sassify a sentence or a word')
            e.add_field(name='>>howgay/gaymeter [member]', value='Check how gay you or your friends are')
            await ctx.send(embed=e)
        elif args == 'mod':
            e = discord.Embed(title='Epic Moderation commands', description='You need the correct permissions for each command. e.g ban_members for banning, manage_roles for muting etc.')
            e.add_field(name='>>ban (@member) [reason]', value='Ban naughty people')
            e.add_field(name='>>unban (user#0000)', value='Unban people that have learned their lesson')
            e.add_field(name='>>mute (@member) [reason]', value='Mute people from chatting in the whole server')
            e.add_field(name='>>unmute (@member)', value='Unmute people after they learn their lesson')
            e.add_field(name='>>kick (@member) [reason]', value='Kicks a member from the server without banning them')
            e.add_field(name='>>purge/clear (2-100)', value='Delete up to 100 messages from the channel')
            e.add_field(name='>>block (@member)', value='Block a member from chatting in the channel this command was used in, without muting the member')
            e.add_field(name='>>unblock (@member)', value='Unblocks member from the channel')
            e.add_field(name='>>user/whois/i/ui (@member)', value='Find out everything about a member')
            e.add_field(name='>>echo/say (channel) (text)', value='Let the bot talk! uwu')
            e.add_field(name='>>guild/server/guildinfo/serverinfo', value='Get server info')
            await ctx.send(embed=e)
        elif args == 'imagegen':
            e = discord.Embed(title='Image generator commands')
            e.add_field(name='>>tweet (username) (tweet)', value='Generate a fake tweet')
            e.add_field(name='>>phcomment (comment)', value='[NSFW CHANNEL ONLY!] Make a fake PHComment ;)')
            await ctx.send(embed=e)
        elif args == 'misc':
            e = discord.Embed(title='Miscellaneous things')
            e.add_field(name='>>ping/latency', value='Get your latency C:')
        else:
            raise commands.BadArgument()

def setup(client):
    client.add_cog(help(client))
