import discord
from discord.ext import commands
import sqlite3

class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages
        if not permission:
            return argument
        else:
            raise commands.BadArgument("You cannot punish other staff members")

class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        muted = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted in argument.roles:
            return argument
        else:
            raise commands.BadArgument("The member was not muted.")

async def mute(ctx, member, reason):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        try:
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels:
                await channel.channel.set_permissions(muted, send_messages=False,
                                                read_message_history=False,
                                                read_messages=False)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role")
        await member.add_roles(muted)
        await ctx.send(f"{member.mention} has been muted for {reason}")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} has been muted for {reason}")

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)

    # ban member
    # Usage: >>ban (member) [reason]
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : Sinner=None, *, reason=None):
        if not member:
            return await ctx.send('You must specify a member to ban')
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member.name} was banned ;-;\nReason: {reason}')
        except discord.Forbidden:
            return await ctx.send('Are you trying to ban someone higher than me? I cant do that ;-;')

    # unban banned member
    # Usage: >>unban (member)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_members = await ctx.guild.bans()
        member_name, member_descriminator = member.split('#')
        for ban_entry in banned_members:
            member = ban_entry.member
            if(member.name, member.discriminator) == (member_name, member_descriminator):
                await ctx.guild.unban(member)
                await ctx.send(f'Sucessfully unbanned {member}')
                print(f'Member unbanned: {member}')
                return

    # mute member
    # Usage: >>mute (member) [reason]
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: Sinner, reason=None):
        """Gives them hell."""
        await mute(ctx, member, reason or "treason")
        await ctx.send(f'{member} was muted for {reason}')

    # unmute member
    # Usage: >>unmute (member)
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: Redeemed):
        """Unmutes a muted member"""
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f"{member.mention} has been unmuted")
        return

    # kick member
    # Usage: >>kick (member) [reason]
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Sinner=None, reason=None):
        if not member:
            return await ctx.send("You must specify a member")
        try:
            await ctx.guild.kick(member, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
            await ctx.send(f'{member} was kicked for {reason}')
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot?")

    # clears chatmessages 
    # Usage: >>purge/clear (limit)
    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        """Bulk deletes messages"""
        # somehow this just works when i do ctx.channel.purge instead of ctx.purge
        await ctx.channel.purge(limit=limit + 1)
        await ctx.channel.send(f"Bulk deleted `{limit}` messages", delete_after=5)

    # block member from sending messages in channel
    # Usage: >>block (member)
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def block(self, ctx, member: Sinner=None):
        if not member:
            return await ctx.send("You must specify a member")
        await ctx.channel.set_permissions(member, send_messages=False)
        await ctx.send(f'{member} was blocked from sending messages in this channel ;-;')

    # unblock member
    # Usage: >>unblock (member)
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unblock(self, ctx, member: Sinner=None):
        if not member:
            return await ctx.send("You must specify a member")
        await ctx.channel.set_permissions(member, send_messages=True)

    # find out member info
    # Usage: >>member/whois/i/ui (member)
    @commands.command(aliases=["member", "whois", "i", "ui"])
    @commands.cooldown(1, 4, commands.BucketType.member)
    async def memberinfo(self, ctx, member: discord.Member = None):
        """Get a members info."""
        if not member:
            member = ctx.message.author
        try:
            playinggame = member.activity.title
        except:
            playinggame = None

        server = ctx.message.guild
        embed = discord.Embed(color=0xDEADBF)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Discriminator", value=member.discriminator)
        embed.add_field(name="Bot", value=str(member.bot))
        embed.add_field(name="Created", value=member.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Joined", value=member.joined_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Animated Avatar", value=str(member.is_avatar_animated()))
        embed.add_field(name="Playing", value=playinggame)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name="Color", value=str(member.color))

        try:
            roles = [x.name for x in member.roles if x.name != "@everyone"]

            if roles:
                roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                            if x.name != "@everyone"].index)
                roles = ", ".join(roles)
            else:
                roles = "None"
            embed.add_field(name="Roles", value=roles)
        except:
            pass

        await ctx.send(embed=embed)

    # let the bot talk uwu
    # Usage: >>echo/say (channel) (text)
    @commands.command(aliases=['say'])
    async def echo(self, ctx, channel:discord.TextChannel=None, *, args):
        # when i tested it it only sends when u give it a channel when u give none it just sends nothing
        try:
            if channel is None:
                return await ctx.send(args)
            elif channel is not None:
                return await channel.send(args)
            else:
                return

        except discord.Forbidden:
            await ctx.send('I dont have permission to talk there ;-;')

    # get server info
    # Usage: >>guild/server/guildinfo/serverinfo 
    @commands.command(aliases=['server', 'guildinfo', 'serverinfo'])
    async def guild(self, ctx):
        await ctx.trigger_typing()

        server = ctx.guild
        roles = []

        for r in server.roles:
            roles.append(r.name)

        stp2 = ", ".join(roles)
        embed = discord.Embed(color=0xFF00EE, title="Guild Info")
        embed.set_author(name=server.name, icon_url=server.icon_url)
        embed.set_footer(text="uwu")
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Name", value=server.name)
        embed.add_field(name="ID", value=str(server.id))
        embed.add_field(name="Roles", value=stp2)
        embed.add_field(name="Owner", value=str(server.owner))
        embed.add_field(name="Members", value=server.member_count)
        embed.add_field(name="Channels", value=len(server.channels))
        embed.add_field(name="Region", value=server.region)
        embed.add_field(name="Custom Emoji", value=len(server.emojis))
        embed.add_field(name="Created At", value=server.created_at)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))
