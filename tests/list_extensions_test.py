#!/usr/bin/env python3
import pytest
import asyncio
from unittest.mock import call, AsyncMock
from discord.ext import commands
from .context import janitor_bot
from janitor_bot import bot


@pytest.mark.asyncio
async def test_list_all_loaded(fs):
    pagination = commands.Paginator()
    extensions = set()
    for i in range(400):
        # create mock cogs
        fs.create_file(f"./cogs/cog{i}.py")
        # create mock extensions
        extensions.add(f"cogs.cog{i}")
        # create expected result
        pagination.add_line(f"cog{i}" + bot.loaded_status)

    ctx_mock = AsyncMock()
    ctx_mock.bot.extensions = extensions

    await bot.list_extensions(ctx_mock)

    calls = []
    for page in pagination.pages:
        calls.append(call(page))

    ctx_mock.send.assert_has_calls(calls)


@pytest.mark.asyncio
async def test_list_all_unloaded(fs):
    pagination = commands.Paginator()
    for i in range(400):
        # create mock cogs
        fs.create_file(f"./cogs/cog{i}.py")
        # create expected result
        pagination.add_line(f"cog{i}" + bot.unloaded_status)

    ctx_mock = AsyncMock()
    # no extensions loaded
    ctx_mock.bot.extensions = {}

    await bot.list_extensions(ctx_mock)

    calls = []
    for page in pagination.pages:
        calls.append(call(page))

    ctx_mock.send.assert_has_calls(calls)


@pytest.mark.asyncio
async def test_list_mixed(fs):
    pagination = commands.Paginator()
    extensions = set()
    for i in range(400):
        # create mock cogs
        fs.create_file(f"./cogs/cog{i}.py")
        # create mock extensions only for odd# cogs
        if i % 2 != 0:
            extensions.add(f"cogs.cog{i}")
            pagination.add_line(f"cog{i}" + bot.loaded_status)
        else:
            pagination.add_line(f"cog{i}" + bot.unloaded_status)

    ctx_mock = AsyncMock()
    ctx_mock.bot.extensions = extensions

    await bot.list_extensions(ctx_mock)

    calls = []
    for page in pagination.pages:
        calls.append(call(page))

    ctx_mock.send.assert_has_calls(calls)


@pytest.mark.asyncio
async def test_empty_list(fs):
    fs.create_dir("cogs")

    ctx_mock = AsyncMock()
    ctx_mock.bot.extensions = []

    await bot.list_extensions(ctx_mock)

    ctx_mock.send.assert_called_with(bot.no_extension_msg)
