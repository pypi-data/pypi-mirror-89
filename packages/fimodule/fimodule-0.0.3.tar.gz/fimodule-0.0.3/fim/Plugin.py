from .url import *
import os
import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import aiohttp
import json
import discord
class Plugin:
    def __init__(self, bot, token):
        self.bot = bot
        self.token = token
    async def httpget(self, weburl, restype="text"):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(weburl) as r:
                if restype == "text":
                    re = await r.text()
                else:
                    re = await r.json()
                return re