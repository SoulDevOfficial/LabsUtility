# Replace temporarily inputs on line #15 & #39.
# Note: This code is not the most recent version. The is just the most recent version that works with the other cog versions :/
import os
import asyncio
import discord
from discord.ext import commands

INTENTS = discord.Intents.default()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=INTENTS,
            application_id=###############
        )

    async def setup_hook(self):
        # Load all cogs from ./cogs
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")

        # Sync globally cause discord doesn't automaticly for some reason 
        await self.tree.sync()

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="discord.gg/rzEfDvDNdJ"
            )
        )
        print(f"Logged in as {self.user} ({self.user.id})")


async def main():
    bot = Bot()
    await bot.start("###################")

asyncio.run(main())
