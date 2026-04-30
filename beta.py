import discord
from discord.ext import commands
import os
import asyncio
from config import PREFIX
from dotenv import load_dotenv
from cogs.ticket import TicketLaunch

load_dotenv()

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix=PREFIX, intents=intents, help_command=None)

    async def setup_hook(self):
        self.add_view(TicketLaunch())
        
        # Chargement des extensions (Cogs)
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_ready(self):
        await self.tree.sync()
        print(f"Connecté en tant que {self.user}")

bot = MyBot()

async def main():
    async with bot:
        await bot.start(os.getenv("BETA_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())