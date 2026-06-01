import discord
from discord.ext import commands
import os
import asyncio
from config import PREFIX
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes synchronisées")
    except Exception as e:
        print(e)
    for cmd in synced:
        print(cmd.name)

    print(f"Connecté en tant que {bot.user}")

async def main():
    async with bot:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())