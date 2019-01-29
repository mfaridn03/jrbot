from discord.ext import commands
import os

extensions = ['Utils', 'Moderation']

desc = "Farid's home-made bot for his personal server"
bot = commands.AutoShardedBot(command_prefix=['f.', 'ff '], description=desc)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}\n"
          f"ID: {bot.user.id}\n"
          f"---------------")

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


if __name__ == '__main__':
    for e in extensions:
        try:
            bot.load_extension(f"cogs.{e}")
            bot.load_extension('jishaku')
        except Exception as er:
            print(f"Failed to load extension {e}:\n{type(er).__name__}: {er}")

bot.run(os.getenv('TOKEN'))
