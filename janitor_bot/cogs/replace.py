from discord.ext import commands
import re

keywords = {}


class Replace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commandPrefix = "!"

    # Event
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or re.search(
            f"^{self.commandPrefix}", message.content
        ):
            return
        new_message = ""
        for word in keywords:
            if re.search(word, message.content):
                new_message = await sendReplacement(message.content)
                await message.delete()
                break
        if new_message != message.content:
            await message.channel.send(f"{message.author} : {new_message}")

    @commands.command()
    async def replace(self, ctx, arg1: str, arg2: str):
        setReplacement(arg1, arg2)


def setup(bot):
    bot.add_cog(Replace(bot))


def sendReplacement(message):
    new_message = message
    for word in keywords:
        new_message = re.sub(word, keywords.get(word), new_message)
    return new_message


def setReplacement(keyword, val):
    global keywords
    keywords[keyword] = val
    keywords = {
        key: value
        for key, value in sorted(
            keywords.items(), key=lambda item: item[0], reverse=True
        )
    }
    return keywords
