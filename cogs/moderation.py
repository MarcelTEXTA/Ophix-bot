import discord
from discord.ext import commands

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commande pour ban
    @commands.hybrid_command(name="ban", help="Bannir un membre du serveur.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Membre banni",
                description=f"{member} a été banni du serveur. Raison: {reason}",
                color=0xED4245
            )
            await ctx.send(embed=embed)

            # DM au membre banni

        except Exception as e:
            await ctx.send(f"Erreur lors du bannissement de {member}: {e}")

    @commands.hybrid_command(name="unban", help="Débannir un membre du serveur.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(user, reason=reason)
            embed = discord.Embed(
                title="🔓 Membre débanni",
                description=f"- `{user}` a été débanni du serveur.\n- `Raison:` {reason}",
                color=0x57F287
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Erreur lors du débannissement de {user}: {e}")
        except 404:
            await ctx.send(f"{user} n'est pas actuellement banni.")


    # command pour kick
    @commands.hybrid_command(name="kick", help="Expulser un membre du serveur.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Membre expulsé",
                description=f"{member} a été expulsé du serveur. Raison: {reason}",
                color=0xED4245
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Erreur lors de l'expulsion de {member}: {e}")

    @commands.hybrid_command(name="unkick", help="Réintégrer un membre expulsé du serveur.")
    @commands.has_permissions(kick_members=True)
    async def unkick(self, ctx, user: discord.User, *, reason=None):
        await ctx.send(f"{ctx.author.mention}, on voit que il ne sera pas un bon modo, on ne peut pas réintégrer un membre expulsé ! On n'est pas le seule à le dire ...")


    # commande pour clear
    @commands.hybrid_command(name="clear", help="Supprimer un nombre de messages dans le salon.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)
            embed = discord.Embed(
                title="🧹 Messages supprimés",
                description=f"{len(deleted)-1} messages ont été supprimés par {ctx.author}.",
                color=0x57F287
            )
            await ctx.send(embed=embed, delete_after=5)
        except Exception as e:
            await ctx.send(f"Erreur lors de la suppression des messages: {e}")


    # commande pour mute
    @commands.hybrid_command(name="mute", help="Rendre un membre muet dans le serveur.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=False)

            await member.add_roles(muted_role, reason=reason)
            embed = discord.Embed(
                title="🔇 Membre muté",
                description=f"{member} a été rendu muet. Raison: {reason}",
                color=0xED4245
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Erreur lors du mutage de {member}: {e}")

    @commands.hybrid_command(name="unmute", help="Rendre un membre non muet dans le serveur.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if muted_role in member.roles:
                await member.remove_roles(muted_role, reason=reason)
                embed = discord.Embed(
                    title="🔊 Membre démute",
                    description=f"{member} a été rendu non muet. Raison: {reason}",
                    color=0x57F287
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{member} n'est pas actuellement muet.")
        except Exception as e:
            await ctx.send(f"Erreur lors du démutage de {member}: {e}")


    # commande pour warn
    @commands.hybrid_command(name="warn", help="Avertir un membre du serveur.")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        try:
            embed = discord.Embed(
                title="⚠️ Avertissement",
                description=f"{member} a été averti. Raison: {reason}",
                color=0xED4245
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Erreur lors de l'avertissement de {member}: {e}")

    @commands.hybrid_command(name="unwarn", help="Retirer un avertissement d'un membre du serveur. Un petit pardon")
    @commands.has_permissions(manage_messages=True)
    async def unwarn(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f"{ctx.author.mention}, on voit que il ne sera pas un bon modo, on ne peut pas retirer un avertissement !")


    # commande


async def setup(bot):
    await bot.add_cog(moderation(bot))