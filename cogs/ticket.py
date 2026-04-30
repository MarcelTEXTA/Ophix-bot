import discord
from discord.ext import commands
from discord import app_commands
import json
import os

# --- GESTION DES DONNÉES ---
CONFIG_FILE = "data/config_tickets.json"
os.makedirs("data", exist_ok=True)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# --- VUE POUR FERMER LE TICKET ---
class TicketControl(discord.ui.View):
    def __init__(self, creator_id: int):
        super().__init__(timeout=None)
        self.creator_id = creator_id

    @discord.ui.button(label="Fermer le Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn", emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("Seul le staff peut fermer ce ticket.", ephemeral=True)

        guild = interaction.guild
        creator = guild.get_member(self.creator_id)
        
        # 1. Envoi du message privé au créateur
        if creator:
            try:
                embed = discord.Embed(
                    title="Ticket Fermé",
                    description=f"Votre ticket sur le serveur **{guild.name}** a été fermé par le staff.",
                    color=discord.Color.red()
                )
                embed.set_image(url="https://votre-image-de-fermeture.png") 
                await creator.send(embed=embed)
            except discord.Forbidden:
                # Si l'utilisateur a bloqué ses DMs
                pass

        # 2. Information dans le salon avant suppression (pour le log visuel)
        await interaction.response.send_message("Le ticket va être supprimé dans 5 secondes...")
        
        # 3. Suppression du salon
        await interaction.channel.delete(reason=f"Ticket fermé par {interaction.user}")

# --- FORMULAIRE DE CONFIGURATION ---
class TicketConfigModal(discord.ui.Modal, title="Configuration du Système"):
    ticket_title = discord.ui.TextInput(label="Titre de l'Embed", default="Support Technique")
    ticket_desc = discord.ui.TextInput(label="Description", style=discord.TextStyle.paragraph)
    welcome_msg = discord.ui.TextInput(label="Message de bienvenue", style=discord.TextStyle.paragraph)
    image_url = discord.ui.TextInput(label="Lien de l'image (vignette)", placeholder="https://...", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        data = load_config()
        guild_id = str(interaction.guild_id)
        
        data[guild_id] = {
            "title": self.ticket_title.value,
            "desc": self.ticket_desc.value,
            "welcome": self.welcome_msg.value,
            "image": self.image_url.value
        }
        save_config(data)
        
        embed = discord.Embed(title=self.ticket_title.value, description=self.ticket_desc.value, color=discord.Color.blue())
        if self.image_url.value:
            embed.set_thumbnail(url=self.image_url.value)
            
        await interaction.response.send_message("✅ Configuration enregistrée !", ephemeral=True)
        await interaction.channel.send(embed=embed, view=TicketLaunch())

# --- LA VUE DU BOUTON D'OUVERTURE ---
class TicketLaunch(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ouvrir un Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket_btn", emoji="📩")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        data = load_config().get(str(guild.id), {})

        welcome_text = data.get("welcome", "Bonjour {user}, comment pouvons-nous vous aider ?")

        category = discord.utils.get(guild.categories, name="Tickets ouverts")
        if category is None:
            category = await guild.create_category("Tickets ouverts")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(name=f"ticket-{user.name}", category=category, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket créé : {channel.mention}", ephemeral=True)
        
        embed_welcome = discord.Embed(
            description=welcome_text.replace("{user}", user.mention),
            color=discord.Color.green()
        )
        await channel.send(embed=embed_welcome, view=TicketControl(creator_id=user.id))

# --- LE COG PRINCIPAL ---
class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket-config", description="Configure le système de ticket")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_config(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketConfigModal())

async def setup(bot):
    await bot.add_cog(Ticket(bot))