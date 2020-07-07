import discord
import re

client = discord.Client();
prefix = "!"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if re.search("^!help$", message.content):
        await message.channel.send('Nah fuck that!')

client.run('NzI5ODgzMTEyNTI3MzY0MTk4.XwPauA.yyQ_n5V8_Sgo-J5Xi2kl_mmhFyY');
