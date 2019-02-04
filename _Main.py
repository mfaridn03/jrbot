from discord.ext import commands
import discord
import os

extensions = ['Fun', 'Moderation']

desc = "Farid's home-made bot for his personal server"
bot = commands.Bot(command_prefix=['f.', 'ff '], description=desc)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}\n"
          f"ID: {bot.user.id}\n"
          f"---------------")
    await bot.change_presence(status=discord.Status.dnd,
                                       activity=discord.Activity(
                                           name="everyone 👀",
                                           type=discord.ActivityType.watching))

@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    
    if msg.channel.id == 534754067998834688 and msg.author.id != 191036924570501120:
        if msg.content.lower().startswith('f.verify') or msg.content.lower().startswith('ff verify'):
            await bot.process_commands(msg)
        else:
            return await msg.delete()
    await bot.process_commands(msg)

@bot.event
async def on_raw_reaction_add(data):
    if data.message_id == 541974797933084702:
        guild = bot.get_guild(data.guild_id)
        member = guild.get_member(data.user_id)
        if data.emoji.name == '🐦':
            role = discord.utils.get(data.roles, id=535346317245808660)
            return await member.add_roles(role)
        if data.emoji.name == '▶':
            role = discord.utils.get(guild.roles, id=535351222543056896)
            return await member.add_roles(role)
        else:
            o = bot.get_user(191036924570501120)
            await o.send(f'Invalid reaction:{data.emoji.name}')

@bot.event
async def on_raw_reaction_remove(data):
    if data.message_id == 541974797933084702:
        guild = bot.get_guild(data.guild_id)
        member = guild.get_member(data.user_id)
        if data.emoji.name == '🐦':
            role = discord.utils.get(guild.roles, id=535346317245808660)
            return await member.remove_roles(role)
        if data.emoji.name == '▶':
            role = discord.utils.get(guild.roles, id=535351222543056896)
            return await member.remove_roles(role)
        else:
            o = bot.get_user(191036924570501120)
            await o.send(f'Invalid reaction:{data.emoji.name}')


if __name__ == '__main__':
    for e in extensions:
        try:
            bot.load_extension(f"cogs.{e}")
            bot.load_extension('jishaku')
        except Exception as er:
            print(f"Failed to load extension {e}:\n{type(er).__name__}: {er}")

bot.run(os.getenv('TOKEN'))  # Nice try
