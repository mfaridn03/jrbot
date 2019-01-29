from discord.ext import commands
import discord
import datetime


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.logging_channel = 537983096633688075

    @commands.has_permissions(kick_members=True)
    @commands.command(mame='kick')
    async def kick(self, ctx, member, *, reason=None):
        """
        Kicks a member

        Example usages:
        - f.kick @BadGuy#1010
        - f.kick 191036924570501120
        - f.kick Sicko#1337 being annoying
        """
        if not reason:
            reason = 'Unspecified'

        try:
            target = await commands.MemberConverter().convert(ctx, member)
        except commands.BadArgument:
            return await ctx.send(f"Member {member} not found")
        
        await target.kick(reason=reason)
        await ctx.send(f"👍 {target} was kicked because of: **{reason}**")
        
        log_channel = discord.utils.get(ctx.guild.channels, id=self.logging_channel)
        emb = discord.Embed(title='Member kick', timestamp=datetime.datetime.utcnow(), colour=discord.Colour.red())
        emb.add_field(name='Member', value=f'{target.mention} ({target} - {target.id})', inline=False)
        emb.add_field(name='Reason', value=reason, inline=False)
        emb.set_footer(text=f'Mod: {ctx.author}', icon_url=ctx.author.avatar_url)
        await log_channel.send(embed=emb)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx, member, *, reason=None):
        """
        Bans member

        Usage examples:
        - f.ban @User#2932 attempted raid
        - f.ban 463962914274148363
        """
        if not reason:
            reason = 'Unspecified'

        try:
            target = await commands.MemberConverter().convert(ctx, member)
        except commands.BadArgument:
            return await ctx.send(f'Member {member} not found')
        
        await ctx.guild.ban(target)
        await ctx.send(f"👍 {target} ({target.id}) was banned because of: **{reason}**")
        
        log_channel = discord.utils.get(ctx.guild.channels, id=self.logging_channel)
        emb = discord.Embed(title='Ban', timestamp=datetime.datetime.utcnow(), colour=discord.Colour.red())
        emb.add_field(name='Member', value=f'{target.mention} ({target} - {target.id})', inline=False)
        emb.add_field(name='Reason', value=reason, inline=False)
        emb.set_footer(text=f'Mod: {ctx.author}', icon_url=ctx.author.avatar_url)
        await log_channel.send(embed=emb)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='unban')
    async def unban(self, ctx, user_id, *, reason=None):
        """
        Unbans a member by their id

        Usage examples:
        - f.unban 326326213624987649 time limit
        - f.unban 298166754331459586
        """
        if not reason:
            reason = 'Unspecified'
        
        entry = ''
        banlist = await ctx.guild.bans()
        for entry in banlist:
            if entry.user.id == user_id:
                user = entry.user
        if user is None:
            return await ctx.send(f'ID **{user_id}** not found')
        await ctx.guild.unban(user)

        log_channel = discord.utils.get(ctx.guild.channels, id=self.logging_channel)
        emb = discord.Embed(title='Unban', timestamp=datetime.datetime.utcnow(), colour=discord.Colour.orange())
        emb.add_field(name='User', value=f'{user.name}#{user.discriminator} ({user.id})', inline=False)
        emb.add_field(name='Reason', value=reason, inline=False)
        emb.set_footer(text=f'Mod: {ctx.author}', icon_url=ctx.author.avatar_url)
        await log_channel.send(embed=emb)


def setup(bot):
    bot.add_cog(Moderation(bot))
