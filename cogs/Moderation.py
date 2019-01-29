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
        
        await target.send(f'You have been kicked out from {ctx.guild.name} for reason: **{reason}**')
        await target.kick(reason=reason)
        await ctx.send(f"👍 {target} was kicked because of: **{reason}**")
        
        log_channel = discord.utils.get(ctx.guild.channels, id=self.logging_channel)
        emb = discord.Embed(title='Member kick', timestamp=datetime.datetime.utcnow(), colour=discord.Colour.red())
        emb.add_field(name='Member', value=f'{target.mention} ({target} - {target.id})', inline=False)
        emb.add_field(name='Reason', value=reason, inline=False)
        emb.set_footer(text=f'Mod: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.message.add_reaction('✅')
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
        
        await target.send(f'You have been banned from {ctx.guild.name} for reason: **{reason}**')
        await ctx.guild.ban(target, reason=reason)
        await ctx.send(f"👍 {target} ({target.id}) was banned because of: **{reason}**")
        
        log_channel = discord.utils.get(ctx.guild.channels, id=self.logging_channel)
        emb = discord.Embed(title='Ban', timestamp=datetime.datetime.utcnow(), colour=discord.Colour.red())
        emb.add_field(name='Member', value=f'{target.mention} ({target} - {target.id})', inline=False)
        emb.add_field(name='Reason', value=reason, inline=False)
        emb.set_footer(text=f'Mod: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.message.add_reaction('✅')
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
        
        user = discord.Object(id=user_id)
        try:
            await ctx.guild.unban(user, reason=reason)
        except discord.NotFound:
            return await ctx.send(f'User {user_id} either cannot be found or is not banned')
        
        log_channel = discord.utils.get(ctx.guild.channels, id=self.logging_channel)
        emb = discord.Embed(title='Unban', timestamp=datetime.datetime.utcnow(), colour=discord.Colour.orange())
        emb.add_field(name='User', value=f'{user.name}#{user.discriminator} ({user.id})', inline=False)
        emb.add_field(name='Reason', value=reason, inline=False)
        emb.set_footer(text=f'Mod: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.message.add_reaction('✅')
        await log_channel.send(embed=emb)
    
    @commands.is_owner()
    @commands.command(name='echo', aliases=['say'], hidden=True)
    async def echo(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(name='verify', hidden=True)
    async def verify(self, ctx):
        if ctx.channel.id != 534754067998834688:
            return

        role = discord.utils.get(ctx.guild.roles, id=534273110023602177)
        await ctx.author.add_roles(role)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Moderation(bot))
