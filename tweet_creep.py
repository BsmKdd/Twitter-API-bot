import os
import logger

from twit_api import tweet_feeder
from bot import bot
from discord.ext import commands

import platform
import asyncio

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    try:
        await ctx.bot.close()
        tweet_feeder.disconnect()
        print("Shut down!")
        exit(1)
    except RuntimeError:
        print(RuntimeError)


def main():
    bot.run(os.environ.get("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
