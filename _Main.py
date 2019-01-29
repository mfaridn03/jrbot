from discord.ext import commands
import os

extensions = ['Utils', 'Moderation']

desc = "Farid's home-made bot for his personal server"
bot = commands.Bot(command_prefix=['f.', 'ff '], description=desc)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}\n"
          f"ID: {bot.user.id}\n"
          f"---------------")


if __name__ == '__main__':
    for e in extensions:
        try:
            bot.load_extension(f"cogs.{e}")
        except Exception as er:
            print(f"Failed to load extension {e}:\n{type(er).__name__}: {er}")

bot.run(os.getenv('TOKEN'))
