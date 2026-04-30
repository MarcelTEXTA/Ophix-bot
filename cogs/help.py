import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche la liste des commandes disponibles")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Aide - Commandes disponibles",
            description="Voici la liste des commandes que vous pouvez utiliser avec Ophix Bot :\n\n"
                        "📌 **/bot-info** : Affiche une introduction du bot.\n"
                        "📌 **/ticket-config** : Configure le système de ticket.\n"
                        "📌 **/help** : Affiche ce message d'aide.\n\n"
                        "N'hésitez pas à essayer ces commandes et à découvrir toutes les fonctionnalités d'Ophix Bot !",
            color=0x57F287
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))