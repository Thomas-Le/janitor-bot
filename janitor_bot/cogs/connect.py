from discord.ext import commands


class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is connected!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.\nUse '!help' to see list of commands.")


def setup(bot):
    bot.add_cog(Connect(bot))
