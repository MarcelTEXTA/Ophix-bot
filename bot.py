import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class OphixBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Listes des cogs"""
        # await self.load_extension("cogs.assistant")
        await self.load_extension("cogs.general")
        # await self.load_extension("cogs.goodbye")
        # await self.load_extension("cogs.ia_bot")
        # await self.load_extension("cogs.welcome")
        # await self.load_extension("cogs.level")
        await self.tree.sync()

bot = OphixBot()

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

bot.run(TOKEN)
