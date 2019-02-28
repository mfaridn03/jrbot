import sqlite3
from discord.ext import commands


class NoCharacter(commands.CheckFailure):
    pass

def has_char():
    def pred(ctx):
        res = ctx.bot.db.execute(
            f'SELECT balance FROM user_balance WHERE userid={ctx.author.id}'
        )
        if res:
            return True
        raise NoCharacter()
   
    return commands.check(pred(ctx))
    
