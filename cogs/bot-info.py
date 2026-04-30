import discord
from discord.ext import commands
from discord import app_commands

class IntroBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bot-info", description="Afficher les informations du bot")
    async def intro(self, interaction: discord.Interaction):
        # Calcul précis du nombre de membres total
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        
        embed = discord.Embed(
            title="Bienvenue sur Ophix Bot !",
            description=(
                "**Généralités**\n"
                f"> Mention : {self.bot.user.mention}\n"
                "> Prefix : `/`\n"
                f"> ID : `{self.bot.user.id}`\n"
                "> Date de mise à jour : 30/04/2026\n\n"

                "**Fonctionnalités**\n"
                "🔹 **Système de ticket** : Ouvrez un ticket pour obtenir de l'aide rapidement.\n"
                "🔹 **Commandes d'assistance** : Guidez vos membres dans votre serveur.\n\n"

                "**Statistiques**\n"
                f"> Serveurs : **{len(self.bot.guilds)}**\n"
                f"> Utilisateurs : **{total_members}**\n\n"

                "**Développement**\n"
                "🔹 **Open Source** : Ophix Bot est un bot open source, développé par la communauté.\n"
                "🔹 **Mise à jour régulière** : Le bot est régulièrement mis à jour."
            ),
            color=0x57F287
        )
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            
        embed.set_footer(text=f"Demandé par {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(IntroBot(bot))