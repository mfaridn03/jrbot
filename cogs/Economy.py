import discord
from discord.ext import commands

moai = "<:moai:532243816946597947>"


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
        async with ctx.typing():
            q = f"INSERT INTO user_info (userid) VALUES {ctx.author.id};" \
            f"INSERT INTO user_balance (balance) VALUES 100;" \
            f"INSERT INTO user_profile (name, multiplier) VALUES ({ctx.author.name}, 1.0);"
            self.bot.db.execute(q, many=True)
        await ctx.send('Profile created!')
    
    @commands.command(name='bal', aliases=['balance'])
    async def balance(self, ctx, member=None):
        """
        Retrieves your (or someone's) balance (server-wide search, not global)
        <member> can be their name#discriminator, id, nickname or username
        
        Usage examples:
        - f.bal
        - f.bal Techno#2329
        - f.bal 376911204481892352
        """
        target = member or str(ctx.author)
        try:
            target = await commands.MemberConverter().convert(
                ctx, target
            )
        except commands.BadArgument:
            return await ctx.send(
                'Cannot find user'
            )
        res = self.bot.db.fetch(
            'SELECT balance FROM user_balance WHERE userid=?', (ctx.author.id,)
        )
        await ctx.send(
            f'`{target}` has **{res}**{moai}'
        )

def setup(bot):
    bot.add_cog(Economy(bot))
    
