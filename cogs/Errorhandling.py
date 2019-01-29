from discord.ext import commands
import discord


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """Error handling module"""

        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'You are on cooldown! Try again in **{commands.CommandOnCooldown.retry_after}s**')

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Missing parameter: **{error.param.name}**')

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send('Command not found')

        elif isinstance(error, commands.NoPrivateMessage):
            return

        elif isinstance(error, commands.NotOwner) or isinstance(error, commands.MissingPermissions):
            return


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
