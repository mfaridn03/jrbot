import asyncio
from datetime import datetime, timezone

import asyncpg
import discord
from discord.ext import commands

moai = "<:moai:532243816946597947>"

def has_char():
    async def predicate(ctx):
        if await ctx.bot.pool.execute(
            'SELECT userid FROM user_info WHERE userid = $1',
            ctx.author.id
        ):
            return True
        raise (NoCharacter(ctx))
    
    return commands.check(predicate)


class NoCharacter(commands.CommandError):
    def __init__(self, ctx):
        super().__init__("You need a character to run this command")
        

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#--#
    async def _is_daily(self, user):
        a = await self.bot.pool.fetchval(
            "SELECT daily_timer FROM user_info WHERE userid = $1",
            user.id
        )
        now = datetime.utcnow()
        diff = int((now - a).total_seconds())
        diff = diff - 86400
        if diff >= 0:
            return diff, True
        return abs(diff), False
    
    async def _set_daily(self, user):
        await self.bot.pool.execute(
            "UPDATE user_info SET daily_timer = $1 WHERE userid = $2",
            datetime.utcnow(),
            user.id
        )
        await self.bot.pool.execute(
            "UPDATE user_profile SET balance = balance + 500 WHERE userid = $2",
            user.id
        )
            
#--#
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
            return await ctx.send(
                "You already have a character!"
            )
        def check(msg):
            return msg.author == ctx.author
        await ctx.send(
            'Enter your profile name (min 3 characters, max 24)'
        )
        try:
            name = await self.bot.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            return await ctx.send(
                'Timeout...'
            )
        if len(name.content) > 24 or len(name.content) < 3:
            return await ctx.send(
                'Name too long or too short!'
            )
        try:
            await self.bot.pool.execute(
                'INSERT INTO user_profile (userid, name) VALUES ($1, $2)',
                ctx.author.id,
                name.content
            )
        except asyncpg.UniqueViolationError:
            return await ctx.send(
                'That name has been taken. Try again with a different name'
            )
        await ctx.send(
            'Profile created!'
        )
    
    @has_char()
    @commands.command(name='daily')  # Placeholder
    async def daily(self, ctx):
        diff, status = await self._is_daily(ctx.author)
        if status:
            await self._set_daily(ctx.author)
            return await ctx.send(
                f'You claimed your daily `500`{moai}'
            )
        h, r = divmod(diff, 3600)
        m, s = divmod(r, 60)
        _, h = divmod(h, 24)
        time_fmt = f"`{h}` hours, `{m}` minutes and `{s}` seconds"
        await ctx.send(
            f"You are on cooldown! Try again in {time_fmt}"
        )
    
    @has_char()
    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, target: str=None):
        """
        Retrieves your balance or another person's balance
        Person search scope is guild-only
        """
        if not target:
            target = ctx.author
        else:
            try:
                target = await commands.MemberConverter().convert(
                    ctx,
                    target
                )
            except commands.CommandError:
                return await ctx.send(
                    'Member not found'
                )
        res = await self.bot.pool.fetchval(
            'SELECT balance FROM user_profile WHERE userid = $1',
            target.id
        )
        if res is None:
            return await ctx.send(
                'Target user has no profile'
            )
        #
        await ctx.send(
            f'{target} has `{res}`{moai}'
        )
        

def setup(bot):
    bot.add_cog(Economy(bot))  # Economy extension not in extensions list. This won't be loaded on purpose
    
