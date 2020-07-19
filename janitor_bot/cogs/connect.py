from discord.ext import commands


class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Event
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is connected!")


def setup(bot):
    bot.add_cog(Connect(bot))
