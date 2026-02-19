from discord.ext import commands
from discord import app_commands
import discord

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- Commande /help ---
    @app_commands.command(name="help", description="Affiche l'aide du bot")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Ophix Bot | Aide",
            description="Voici les commandes disponibles :",
            color=0x5865F2
        )
        embed.add_field(name="/help", value="Affiche ce message", inline=False)
        embed.add_field(name="/set-auto-welcome", value="Configure le message de bienvenue", inline=False)
        embed.add_field(name="/set-auto-goodbye", value="Configure le message d'au revoir", inline=False)
        embed.add_field(name="/set-auto-level", value="Configure le message de level up", inline=False)
        embed.add_field(name="/set-auto-message", value="Configure un message automatique", inline=False)
        embed.add_field(name="/set-auto-assistant", value="Configure le message de l'assistant", inline=False)
        embed.add_field(name="/ia", value="Pose une question à l'assistant", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # --- Commande /ping ---
    @app_commands.command(name="ping", description="Teste la latence du bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🏓 Pong ! {round(self.bot.latency * 1000)}ms")

    # --- Commande Welcome ---
    @app_commands.command(name="welcome", description="Affiche un message de bienvenue")
    async def welcome_command(self, interaction: discord.integrations):
        embed = discord.Embed(
            title="Bienvenue sur le serveur !",
            description="Nous sommes ravis de t'accueillir parmi nous ! N'hésite pas à te présenter et à participer aux discussions !",
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


# Fonction d'initialisation du cog

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
