import discord
from discord.ext import commands

LOG_CHANNEL_ID = 1465962171685933068

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() # Pour ajout de serveur
    async def on_guild_join(self, guild: discord.Guild):
        try:
            channel = self.bot.get_channel(LOG_CHANNEL_ID)

            if channel is None:
                channel = await self.bot.fetch_channel(LOG_CHANNEL_ID)

            embed = discord.Embed(
                title="📥 Nouveau serveur",
                color=0x57F287
            )

            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            embed.add_field(
                name="Nom",
                value=guild.name,
                inline=False
            )

            embed.add_field(
                name="ID",
                value=str(guild.id),
                inline=False
            )

            embed.add_field(
                name="Membres",
                value=str(guild.member_count),
                inline=False
            )

            owner = guild.owner

            if owner:
                embed.add_field(
                    name="Propriétaire",
                    value=(owner.id), # prolème identifié ici
                    inline=False
                )
            else:
                embed.add_field(
                    name="Propriétaire",
                    value="Inconnu",
                    inline=False
                )

            embed.add_field(
                name="Nombre total de serveurs",
                value=str(len(self.bot.guilds)),
                inline=False
            )

            embed.set_footer(
                text=f"Bot ID : {self.bot.user.id}"
            )

            await channel.send(embed=embed)

        except Exception as e:
            print(f"[ERREUR on_guild_join] {e}")

    @commands.Cog.listener() # Pour suppression de serveur
    async def on_guild_remove(self, guild: discord.Guild):
        try:
            channel = self.bot.get_channel(LOG_CHANNEL_ID)

            if channel is None:
                channel = await self.bot.fetch_channel(LOG_CHANNEL_ID)

            embed = discord.Embed(
                title="📤 Serveur quitté",
                color=0xED4245
            )

            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)

            embed.add_field(
                name="Nom",
                value=guild.name,
                inline=False
            )

            embed.add_field(
                name="ID",
                value=str(guild.id),
                inline=False
            )

            embed.add_field(
                name="Membres",
                value=str(guild.member_count),
                inline=False
            )

            owner = guild.owner

            if owner:
                embed.add_field(
                    name="Propriétaire",
                    value=f"{owner} ({owner.id})",
                    inline=False
                )

            embed.add_field(
                name="Nombre total de serveurs",
                value=str(len(self.bot.guilds)),
                inline=False
            )

            embed.set_footer(
                text=f"Bot ID : {self.bot.user.id}"
            )

            await channel.send(embed=embed)

        except Exception as e:
            print(f"[ERREUR on_guild_remove] {e}")

async def setup(bot):
    await bot.add_cog(Logs(bot))