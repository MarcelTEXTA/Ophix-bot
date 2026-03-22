import discord
from discord.ext import commands
from discord import app_commands
import json
import os

CONFIG_FILE = "data/config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Assistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # STAFF → config message
    # =========================
    @app_commands.command(name="set-intro", description="Définir le message d'introduction")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_intro(self, interaction: discord.Interaction, message: str):

        data = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in data:
            data[guild_id] = {"intro": "", "buttons": []}

        data[guild_id]["intro"] = message
        save_config(data)

        await interaction.response.send_message("✅ Intro définie", ephemeral=True)

    # =========================
    # STAFF → ajouter bouton
    # =========================
    @app_commands.command(name="add-button", description="Ajouter un bouton")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_button(
        self,
        interaction: discord.Interaction,
        label: str,
        message: str
    ):

        data = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in data:
            data[guild_id] = {"intro": "", "buttons": []}

        data[guild_id]["buttons"].append({
            "label": label,
            "message": message
        })

        save_config(data)

        await interaction.response.send_message("✅ Bouton ajouté", ephemeral=True)

    # =========================
    # UTILISATEUR → UI dynamique
    # =========================
    @app_commands.command(name="help-support", description="Ouvrir l'assistant")
    async def help_support(self, interaction: discord.Interaction):

        data = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in data:
            await interaction.response.send_message(
                "⚠️ Aucun assistant configuré sur ce serveur.",
                ephemeral=True
            )
            return

        config = data[guild_id]

        embed = discord.Embed(
            title="🤖 Assistant",
            description=config["intro"],
            color=0x5865F2
        )

        view = discord.ui.View()

        for btn_data in config["buttons"]:

            button = discord.ui.Button(
                label=btn_data["label"],
                style=discord.ButtonStyle.primary
            )

            async def callback(interaction, msg=btn_data["message"]):
                await interaction.response.send_message(msg, ephemeral=True)

            button.callback = callback
            view.add_item(button)

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Assistant(bot))