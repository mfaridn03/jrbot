import discord


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        bot_role = discord.utils.get(member.guild.roles, name='Bot')
        if member.bot:
            return await member.add_roles(bot_role)


def setup(bot):
    bot.add_cog(Events(bot))
