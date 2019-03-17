import datetime
import json
import os
import traceback

import asyncpg
from discord.ext import commands
import discord

desc = "Farid's home-made bot for his personal server"
extensions = ['cogs.Fun', 'cogs.Info', 'cogs.Economy', 'jishaku']

token = os.getenv('TOKEN')
p = ['f.', 'ff ', 'f!']


class JrBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(*p),
            case_insensitive=True,
            description=desc,
            reconnect=True,
            fetch_offline_members=True,
            status=discord.Status.idle,
            activity=discord.Activity(
                name='myself booting...',
                type=discord.ActivityType.watching
            )
        )
        self.last_boot = datetime.datetime.utcnow()
        self.commands_used = 0
        self.beta_id = 550602719325585408
        self.stable_id = 537570246626902016
        self.config = json.loads(os.getenv('config'))
        self.pool = None
#--#
    async def init_db(self):
        self.pool = await asyncpg.create_pool(dsn=self.config['DATABASE_URL'])
        with open("setup/schema.sql") as o:
            await self.pool.execute(o.read())
#--#
    async def start(self):
        for extension in extensions:
            try:
                self.load_extension(extension)
                print(f'{extension} loaded!')
            except:
                print(traceback.format_exc())
        await super().start(token)  # Nice try skids
#--#
    async def on_command_completion(self, ctx):
        self.commands_used += 1
        await self.pool.execute(
            'UPDATE commands SET total_commands = total_commands + 1'
        )
#--#
    async def on_ready(self):
        await self.init_db()
        print('Database connection initialised!')
        
        _activity = discord.Activity(
            name='f.help',
            type=discord.ActivityType.watching
        )
        
        if self.user.id == self.beta_id:
            _activity = discord.Streaming(
                name='f!help',
                url='https://www.twitch.tv/whydoyouclickonthis',
                details='mention me!'
            )
            
        await self.change_presence(
            status=discord.Status.dnd,
            activity=_activity
        )
        print(f"\n---------------\n"
              f"Logged in as {self.user}\n"
              f"ID: {self.user.id}\n"
              f"---------------")
#--#
    async def on_message(self, msg):
        ctx = await self.get_context(msg)

        if ctx.author.bot:
            return

        if (
            ctx.channel.id == 534754067998834688 and
            ctx.author.id != 191036924570501120
        ):
            if (
                msg.content.lower().startswith('f.verify') or
                msg.content.lower().startswith('ff verify')
            ):
                await self.process_commands(msg)
            else:
                return await msg.delete()
        if msg.content == '<@550602719325585408>' and self.user.id == self.beta_id:
            return await ctx.send(
                'Hello there! My prefix is: `f!`\nor when mentioned'
            )
        
        if msg.content == '<@537570246626902016>' and self.user.id == self.stable_id:
            return await ctx.send(
                'Hello there! My prefix is: `f.`\n`ff `\nor when mentioned'
            )
        
        if (
            msg.content.startswith('f!') or
            msg.content.startswith('<@550602719325585408>')
        ) and self.user.id == self.beta_id:
            await self.process_commands(msg)
            
        if (
            (
                msg.content.startswith('f.') or
                msg.content.startswith('ff ') or
                msg.content.startswith('<@537570246626902016>')
            )
            and self.user.id == self.stable_id
        ):
            await self.process_commands(msg)
#--#
    async def process_commands(self, msg):
        ctx = await self.get_context(msg)
        if ctx.command is None:
            return
        
        await self.invoke(ctx)
#--#
    async def on_raw_reaction_add(self, data):
        if data.message_id == 541974797933084702:
            guild = self.get_guild(data.guild_id)
            member = guild.get_member(data.user_id)
            if data.emoji.name == '🐦':
                role = discord.utils.get(guild.roles, id=535346317245808660)
                return await member.add_roles(role)
            if data.emoji.name == '▶':
                role = discord.utils.get(guild.roles, id=535351222543056896)
                return await member.add_roles(role)
            else:
                o = self.get_user(191036924570501120)
                await o.send(f'Invalid reaction:{data.emoji.name}')

    async def on_raw_reaction_remove(self, data):
        if data.message_id == 541974797933084702:
            guild = self.get_guild(data.guild_id)
            member = guild.get_member(data.user_id)
            if data.emoji.name == '🐦':
                role = discord.utils.get(guild.roles, id=535346317245808660)
                return await member.remove_roles(role)
            if data.emoji.name == '▶':
                role = discord.utils.get(guild.roles, id=535351222543056896)
                return await member.remove_roles(role)
            else:
                o = self.get_user(191036924570501120)
                await o.send(f'Invalid reaction:{data.emoji.name}')


if __name__ == '__main__':
    JrBot().run()
