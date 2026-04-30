import discord
from discord.ext import commands

LOG_CHANNEL_ID = 1465962171685933068 # support

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        channel = self.bot.get_channel(LOG_CHANNEL_ID)

        if not channel:
            return

        embed = discord.Embed(
            title="📥 Nouveau serveur",
            color=0x57F287
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Nom", value=guild.name, inline=False)
        embed.add_field(name="ID", value=guild.id, inline=False)
        embed.add_field(name="Membres", value=guild.member_count, inline=False)
        embed.add_field(name="Nous sommes dans :", value=f"{len(self.bot.guilds)} serveurs", inline=True)

        if guild.owner:
            embed.add_field(
                name="Owner",
                value=f"{guild.owner} ({guild.owner.id})",
                inline=False
            )

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))