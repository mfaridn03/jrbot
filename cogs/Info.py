import datetime
import os
import time

from discord.ext import commands
import discord
import psutil

online_id = 548809986676097035
offline_id = 548809987086876672
dnd_id = 548809987212705802
idle_id = 548809986982281266


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.online = self.bot.get_emoji(online_id)
        self.offline = self.bot.get_emoji(offline_id)
        self.dnd = self.bot.get_emoji(dnd_id)
        self.idle = self.bot.get_emoji(idle_id)
    
    @commands.command(name='invite')
    async def invite(self, ctx):
        """Invite me!"""
        invite_link = "https://discordapp.com/api/oauth2/authorize?client_id=537570246626902016&permissions=470154305&scope=bot"
        emb = discord.Embed(title=discord.Embed.Empty,
                            description=invite_link)
        emb.set_author(name='Invite me!')
        emb.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=emb)
        
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
  
        roles = '\n'.join([role.mention for role in m.roles[::-1]])
        role_desc = "Roles (highest to lowest)"
        if len(str(roles)) > 512:
            role_desc = "Top 5 roles (highest to lowest, because too many roles)"
            roles = '\n'.join([role.mention for role in m.roles[::-1][:5]])

        joined = str(m.joined_at.strftime('%d-%m-%Y\n%I:%M:%S %p'))
        created = str(m.created_at.strftime('%d-%m-%Y\n%I:%M:%S %p'))

        emb = discord.Embed(title=f'Info on {username}',
                            description=f'**Display name:** {display_name}',
                            colour=col,
                            timestamp=datetime.datetime.utcnow())
        emb.add_field(name='User ID', value=str(uid))
        emb.add_field(name='Bot user?', value=is_bot)
        emb.add_field(name=role_desc, value=roles)
        emb.add_field(name=f'Joined this server at', value=joined)
        emb.add_field(name='Created at', value=created)
        emb.set_thumbnail(url=avatar)
        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        
        if m.id == 537570246626902016:
            emb.set_author(name="Ayy lmao. It's me")
        
        if m.id == 191036924570501120:
            emb.set_author(name="My master (creator of this bot)")

        await ctx.send(embed=emb)

    @commands.command(name='serverinfo', aliases=['server'])
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
        created_at = str(guild.created_at.strftime('%d-%m-%Y\n%I:%M:%S %p'))
        roles = f"{len(guild.roles)}\nTop role: {guild.roles[-1].mention}"
        icon = guild.icon_url
        verif = guild.verification_level
        vc_region = guild.region
        content_filter = guild.explicit_content_filter
        internals = f"Verification level: {verif}\nVoice region: {vc_region}\nContent filter: {content_filter}"
        
        onliners = len([a for a in ctx.guild.members if str(a.status) == 'online'])
        offliners = len([a for a in ctx.guild.members if str(a.status) == 'offline'])
        dnders = len([a for a in ctx.guild.members if str(a.status) == 'dnd'])
        idlers = len([a for a in ctx.guild.members if str(a.status) == 'idle'])
        
        member_status = f"\n{self.online}{onliners}  {self.offline}{offliners}  {self.dnd}{dnders}  {self.idle}{idlers}"
        members += member_status

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
        target = member or ctx.author.id
        try:
            m = await commands.MemberConverter().convert(ctx, targ)
        except commands.BadArgument:
            return await ctx.send(f'Member {member} not found')

        desc = f'[Link]({m.avatar_url})'
        emb = discord.Embed(title=f"{str(m)}'s avatar",
                            description=desc,
                            colour=m.colour)
        emb.set_image(url=m.avatar_url)
        await ctx.send(embed=emb)
    
    @commands.command(name='bot', aliases=['botinfo'])
    async def botinfo(self, ctx):
        """
        Retrieves info about the bot
        """
        process = psutil.Process(os.getpid())
        
        cpu = process.cpu_percent() / psutil.cpu_count()
        memory = round((process.memory_full_info().uss / (1024 ** 2)), 2)
        py = f"[discord.py - rewrite](https://github.com/Rapptz/discord.py/tree/rewrite)"
        ver = 'Python 3.6.6'
        members = len(self.bot.users)
        servers = len(self.bot.guilds)
        now = datetime.datetime.utcnow()
        uptime = now - self.bot.last_boot
        h, r = divmod(int(uptime.total_seconds()), 3600)
        m, s = divmod(r, 60)
        d, h = divmod(h, 24)
        
        owner = discord.utils.get(self.bot.users, id=191036924570501120)
        
        emb = discord.Embed(
            title='Bot information',
            colour=ctx.me.colour,
            timestamp=datetime.datetime.utcnow()
        )
        emb.add_field(
            name='Created by',
            value=f'{owner.mention} ({owner})'
        )
        emb.add_field(
            name='Library',
            value=f"{py}\nVersion: {ver}"
        )
        emb.add_field(
            name='CPU usage',
            value=f"{cpu}%"
        )
        emb.add_field(
            name='Memory usage',
            value=f"{memory} MiB"
        )
        emb.add_field(
            name='Stats',
            value=f"Servers: {servers}\nMembers: {members}"
        )
        emb.add_field(
            name='Commands since last boot', value=self.bot.commands_used
        )
        emb.add_field(
            name='Uptime',
            value=f'`{d}` days, `{h}` hours, `{m}` minutes, `{s}` seconds'
        )
        emb.set_footer(
            text=ctx.author,
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=emb)
#--#
    @commands.command(name='ping', aliases=['pong'])
    async def ping(self, ctx):
        """Measure the bot's latency"""
        before = time.perf_counter()
        await ctx.trigger_typing()
        after = time.perf_counter()
        
        typing = f"**Typing**: `{round((after-before) * 1000)}`ms"
        latency = f"**Websocket**: `{round(self.bot.latency * 1000)}`ms"
        msg = f"{latency}\n{typing}"
        
        sent = time.perf_counter()
        m = await ctx.send(
            "Pong! :ping_pong:\n"
        )
        await m.edit(
            content=f"Pong! :ping_pong:\n{msg}\n**Edit**: `{round((time.perf_counter() - sent) * 1000)}`ms"
        )
#--#

    @commands.command(name='roleinfo')
    async def roleinfo(self, ctx, role=None):
        """
        Fetch info about a role
        <role> can be its name, id or mention
        """
        if not role:
            return await ctx.send('No role provided')
        try:
            r = await commands.RoleConverter().convert(ctx, role)
        except commands.BadArgument:
            return await ctx.send(f'Role `{role}` not found')
        
        perms = ''
        if r.permissions.administrator:
            perms = 'Administrator'
        else:
            for p in r.permissions:
                x, y = p
                if y:
                    perms += f'{x}, '
        
        perm_value = str(r.permissions.value)
        colour = str(r.colour)
        integrated = r.managed
        created_at = r.created_at.strftime('%d-%m-%Y\n%I:%M:%S %p')
        members = len(r.members)
        
        emb = discord.Embed(
            title=str(r),
            colour=r.colour,
            description=f'{r.mention}\n**ID**: {r.id}\n**Permissions**:\n{perms}'
        )
        emb.add_field(
            name='Value',
            value=perm_value
        )
        emb.add_field(
            name='Colour',
            value=colour
        )
        emb.add_field(
            name='Integrated/managed?',
            value=integrated
        )
        emb.add_field(
            name='Created at',
            value=created_at
        )
        emb.add_field(
            name='Members with this role',
            value=members
        )
        emb.set_footer(
            text=ctx.author,
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=emb)
        

def setup(bot):
    bot.add_cog(Info(bot))
