import asyncio

import asyncpg
import discord
from discord.ext import commands

moai = "<:moai:532243816946597947>"

def has_char():
    async def predicate(ctx):
        if await ctx.bot.pool.execute(
            'SELECT userid FROM user_profile WHERE userid = $1',
            ctx.author.id
        ):
            return True
        raise (NoCharacter(ctx))
    
    return commands.check(predicate)


class NoCharacter(commands.CommandError):
    def __init__(self, ctx):
        super().__init__("You need a character for this")
        

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
        if await self.bot.pool.fetchrow(
            "SELECT userid from user_profile where userid = $1",
            ctx.author.id
        ):
            return await ctx.send("You already have a character!")
        
        def check(msg):
            return msg.author == ctx.author
        
        await ctx.send('Enter your profile name (min 3 characters, max 24)')
        
        try:
            name = await self.bot.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            return await ctx.send('Timeout...')
        
        if len(name.content) > 24 or len(name.content) < 3:
            return await ctx.send('Name too long or too short!')
        
        try:
            await self.bot.pool.execute(
                'INSERT INTO user_profile (userid, name) VALUES ($1, $2)',
                ctx.author.id,
                name.content
            )
        except asyncpg.UniqueViolationError:
            return await ctx.send('That name has been taken. Try again with a different name')
        await ctx.send('Profile created!')
    
    @commands.command(name='free')  # Placeholder
    async def free(self, ctx):
        await self.bot.pool.execute(
            "UPDATE user_profile SET balance = balance + 500 WHERE userid=$1",
            ctx.author.id
        )
        
        

def setup(bot):
    bot.add_cog(Economy(bot))  # Economy extension not in extensions list. This won't be loaded on purpose
    
