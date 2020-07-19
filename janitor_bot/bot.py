#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from discord.ext import commands
from config import *

loaded_status = " [loaded]"
unloaded_status = " [unloaded]"
no_extension_msg = "```No extensions found```"
bot = commands.Bot(command_prefix="!")


@bot.command(help="Loads an extension")
async def load(ctx, extension):
    try:
        ctx.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded extension: {extension}")
    except commands.ExtensionNotFound:
        await ctx.send(
            "Unable to load extension: **Extension not found**\nUse '!list-extensions' command to see list of loaded and unloaded extensions"
        )
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"'{extension}' already loaded")


@bot.command(help="Unloads an extension")
async def unload(ctx, extension):
    try:
        ctx.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded extension: {extension}")
    except commands.ExtensionNotLoaded:
        await ctx.send(
            "Unable to unload extension: **Extension not loaded**\nUse '!list-extensions' command to see list of loaded and unloaded extensions"
        )


@bot.command(help="Reloads an extension")
async def reload(ctx, extension):
    try:
        ctx.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded extension: {extension}")
    except commands.ExtensionNotLoaded:
        await ctx.send(
            "Unable to reload extension: **Extension not loaded**\nUse '!list-extensions' command to see list of loaded and unloaded extensions"
        )


@bot.command(
    name="list-extensions",
    help="List all extensions and their status (unloaded/loaded)",
)
async def list_extensions(ctx):
    pagination = commands.Paginator()
    cog_dir = os.listdir("./cogs")

    for file in cog_dir:
        if file.endswith(".py"):
            file = file[:-3]
            if f"cogs.{file}" in ctx.bot.extensions:
                pagination.add_line(line=file + loaded_status)
            else:
                pagination.add_line(line=file + unloaded_status)

    if len(pagination.pages) == 0:
        await ctx.send(no_extension_msg)
    else:
        for page in pagination.pages:
            await ctx.send(page)


if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(DISCORD_TOKEN)
