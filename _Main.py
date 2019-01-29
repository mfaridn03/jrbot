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
    if msg.channel.id == 534754067998834688 and (
        msg.content.lower() != 'f.verify' or msg.content.lower() != 'ff verify'):
        return await msg.delete()
    else:
        await bot.process_commands(msg)


if __name__ == '__main__':
    for e in extensions:
        try:
            bot.load_extension(f"cogs.{e}")
            bot.load_extension('jishaku')
        except Exception as er:
            print(f"Failed to load extension {e}:\n{type(er).__name__}: {er}")

bot.run(os.getenv('TOKEN'))
