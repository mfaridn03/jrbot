import discord
from discord.ext import commands


class Economy(commands.Cog):
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
    
