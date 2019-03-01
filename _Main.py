from discord.ext import commands
import discord
import os
import traceback
import datetime

desc = "Farid's home-made bot for his personal server"
extensions = ['cogs.Fun', 'cogs.Info', 'jishaku']

token = os.getenv('TOKEN')

class JrBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=['f.', 'ff '],
            case_insensitive=True,
            description=desc,
            reconnect=True,
            status=discord.Status.idle,
            activity=discord.Activity(
                name='myself booting...',
                type=discord.ActivityType.watching
            )
        )
        self.last_boot = datetime.datetime.utcnow()
        self.commands_used = 0

    async def start(self):
        for extension in extensions:
            try:
                self.load_extension(extension)
                print(f'{extension} loaded!')
            except:
                print(traceback.format_exc())
        print('-----')
        await super().start(token)  # Nice try skids

    async def on_command_completion(self, ctx):
        self.commands_used += 1

    async def on_ready(self):
        print(f"Logged in as {self.user}\n"
              f"ID: {self.user.id}\n"
              f"---------------")
        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                name='everyone 👀',
                type=discord.ActivityType.watching
            )
        )
#--#
    async def on_message(self, msg):
        ctx = await self.get_context(msg)

        if ctx.author.bot:
            return

        if (
                ctx.channel.id == 534754067998834688 and ctx.author.id != 191036924570501120
        ):
            if msg.content.lower().startswith('f.verify') or msg.content.lower().startswith('ff verify'):
                await self.process_commands(msg)
            else:
                return await msg.delete()

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
