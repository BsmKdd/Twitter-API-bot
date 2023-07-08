"""
a
"""
import discord
import json
import os
from discord.ext import commands

activity = discord.Activity(
    type=discord.ActivityType.watching, name="Twitter Accounts"
)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", activity=activity, intents=intents)
client = discord.Client(intents=intents)

accounts_file = open("accounts.json", encoding="utf-8")
accounts_dict = json.load(accounts_file)
accounts = list(list(accounts_dict.values()))
accounts_file.close()


@bot.event
async def push_message(message):
    """
    a
    """
    await bot.wait_until_ready()

    poe_channel = bot.get_channel(int(os.environ.get("DISCORD_POE_CHANNEL_ID")))

    if not bot.is_closed():
        await poe_channel.send(message)


@bot.event
async def on_ready():
    """
    a
    """
    print(f"{bot.user} Ready!")
