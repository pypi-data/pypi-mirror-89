import .url
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
    async def 