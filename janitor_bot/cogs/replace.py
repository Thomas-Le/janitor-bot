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
        new_message = message.content
        for word in keywords:
            if re.search(word, message.content):
                new_message = sendReplacement(message.content)
                await message.delete()
                break
        if new_message != message.content:
            await message.channel.send(f"{message.author} : {new_message}")

    @commands.command(
        help="Command janitor bot to replace the first specified word with the second in all future messages.\nStop replacements with '!end-replacement <arg1>'"
    )
    async def replace(self, ctx, arg1: str, arg2: str):
        setReplacement(arg1, arg2)

    @replace.error
    async def replace_error(self, ctx, error):
        await ctx.send(f"{error} Use '!help replace' for more info.")

    @commands.command(
        name="end-replacement", help="Command janitor bot to stop replacing a word."
    )
    async def end_replacement(self, ctx, arg1: str):
        remove_replacement(arg1)

    @end_replacement.error
    async def end_replacement_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"{error.original}")
        else:
            await ctx.send(f"{error} Use '!help end-replacement' for more info.")


def setup(bot):
    bot.add_cog(Replace(bot))


def sendReplacement(message):
    new_message = message
    for word in keywords:
        new_message = re.sub(word, keywords.get(word), new_message)
    return new_message


def remove_replacement(keyword):
    global keywords
    try:
        keywords.pop(keyword)
    except KeyError:
        raise commands.CommandInvokeError(
            "I am currently not replacing that word!\nUse '!show-replacements' to see a list of words and their replacement."
        )


def setReplacement(keyword, val):
    global keywords
    keywords[keyword] = val
    sort_dict()

def sort_dict():
    global keywords
    keywords = {
        key: value
        for key, value in sorted(
            keywords.items(), key=lambda item: item[0], reverse=True
        )
    }
