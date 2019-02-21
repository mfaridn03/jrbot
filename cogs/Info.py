from discord.ext import commands
import discord
import datetime


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='verify', hidden=True)
    async def verify(self, ctx):
        if ctx.channel.id != 534754067998834688:
            return

        role = discord.utils.get(ctx.guild.roles, id=534273110023602177)
        await ctx.author.add_roles(role)
        await ctx.message.delete()

    @commands.command(name='info', aliases=['userinfo'])
    async def userinfo(self, ctx, *, member=None):
        """
        Retrieves info about yourself, or a user
        <member> is optional

        Usage examples:
        - f.info
        - f.info Sai#8985
        - f.info Tiger
        """
        if member:
            try:
                m = await commands.MemberConverter().convert(ctx, member)
            except commands.BadArgument:
                return await ctx.send(f'Member {member} not found')
        else:
            m = ctx.author

        username = str(m)
        display_name = m.display_name
        col = m.colour
        uid = m.id
        avatar = m.avatar_url
        is_bot = m.bot
        roles = ' '.join([role.mention for role in m.roles])
        joined = str(m.joined_at)[:10]
        created = str(m.created_at)[:10]

        emb = discord.Embed(title=f'Info on {username}',
                            description=f'**Display name:** {display_name}',
                            colour=col,
                            timestamp=datetime.datetime.utcnow())
        emb.add_field(name='User ID', value=str(uid))
        emb.add_field(name='Bot user?', value=is_bot)
        emb.add_field(name='Roles (lowest to highest)', value=roles)
        emb.add_field(name=f'Joined {ctx.guild.name} at', value=joined)
        emb.add_field(name='Created at', value=created)
        emb.set_thumbnail(url=avatar)
        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=emb)

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        """
        Retrieves server info

        Usage:
        - f.serverinfo
        """
        guild = ctx.guild
        name = guild.name
        afk = str(guild.afk_channel)
        owner = guild.owner.mention
        text_channels = len(guild.text_channels)
        vc = len(guild.voice_channels)
        channels = f"Total: {text_channels + vc}\nText channels: {text_channels}\nVoice channels: {vc}"
        channels += f"\nNSFW channels: {len([n for n in guild.text_channels if n.is_nsfw()])}"
        members = f"Total: {len(guild.members)}"
        members += f"\nHumans: {len([h for h in guild.members if not h.bot])}"
        members += f"\nBots: {len([b for b in guild.members if b.bot])}"
        created_at = str(guild.created_at)[:10]
        roles = f"{len(guild.roles)}\nTop role: {guild.roles[-1].mention}"
        icon = guild.icon_url
        verif = guild.verification_level
        vc_region = guild.region
        content_filter = guild.explicit_content_filter
        internals = f"Verification level: {verif}\nVoice region: {vc_region}\nContent filter: {content_filter}"

        emb = discord.Embed(title='Server info',
                            description=f'**Name:** {name}\n**ID**: {guild.id}',
                            colour=discord.Colour.dark_teal(),
                            timestamp=datetime.datetime.utcnow())
        emb.add_field(name='Owner', value=owner)
        emb.add_field(name='Created at', value=created_at)
        emb.add_field(name='Internals', value=internals)
        emb.add_field(name='AFK Channel', value=afk)
        emb.add_field(name='Channels', value=channels)
        emb.add_field(name='Members', value=members)
        emb.add_field(name='Roles', value=roles)
        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        if 'icon' in icon:
            emb.set_thumbnail(url=icon)

        await ctx.send(embed=emb)

    @commands.command(name='avatar')
    async def avatar(self, ctx, member=None):
        """
        Get the avatar of yourself or a member

        Usage examples:
        - f.avatar
        - f.avatar John12
        - f.avatar 235148962103951360
        - f.avatar @Farid#0001
        """
        if member:
            try:
                m = await commands.MemberConverter().convert(ctx, member)
            except commands.BadArgument:
                return await ctx.send(f'Member {member} not found')
        else:
            m = ctx.author

        desc = f'[Link]({m.avatar_url})'
        emb = discord.Embed(title=f"{str(m)}'s avatar",
                            description=desc,
                            colour=m.colour)
        emb.set_image(url=m.avatar_url)
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Info(bot))
