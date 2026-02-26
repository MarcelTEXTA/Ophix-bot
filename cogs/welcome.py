from discord.ext import commands
from discord import app_commands
import discord

class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- Commande /set-auto-welcome ---
    @app_commands.command(name="set-auto-welcome", description="Configure le message de bienvenue")
    async def set_auto_welcome_command(self, interaction: discord.Interaction, message: str):
        # logique pour enregistrer le message de bienvenue dans la base de données ou la configuration du bot
        await interaction.response.send_message(f"Configurer le message de bienvenue : {message}")



# Fonction d'initialisation du cog
async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))