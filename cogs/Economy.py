import discord
from discord.ext import commands
import sqlite3
from utils import checks

conn = sqlite3.connect('Data.db')
c = conn.cursor()

class Economy:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='create')
    async def create(self, ctx):
        """
        Create your profile
        
        Usage:
        - f.create
        """
        pass

def setup(bot):
    bot.add_cog(Economy(bot))
    
