import discord
from discord.ext import commands
from discord import app_commands


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------- USER ----------

    @app_commands.command(name="user-avatar", description="Get a user's avatar")
    async def user_avatar(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None
    ):
        user = user or interaction.user

        embed = discord.Embed(title=f"{user}'s Avatar", color=discord.Color.blurple())
        embed.set_image(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="user-banner", description="Get a user's banner")
    async def user_banner(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None
    ):
        user = user or interaction.user

        if not user.banner:
            await interaction.response.send_message(
                "This user does not have a banner.",
                ephemeral=True
            )
            return

        embed = discord.Embed(title=f"{user}'s Banner", color=discord.Color.blurple())
        embed.set_image(url=user.banner.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ---------- SERVER ----------

    @app_commands.command(name="server-info", description="Get server information")
    async def server_info(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.blurple()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="Server ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"))

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="server-icon", description="Get the server icon")
    async def server_icon(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild or not guild.icon:
            await interaction.response.send_message(
                "This server does not have an icon.",
                ephemeral=True
            )
            return

        embed = discord.Embed(title=f"{guild.name} Icon", color=discord.Color.blurple())
        embed.set_image(url=guild.icon.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="server-banner", description="Get the server banner")
    async def server_banner(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild or not guild.banner:
            await interaction.response.send_message(
                "This server does not have a banner.",
                ephemeral=True
            )
            return

        embed = discord.Embed(title=f"{guild.name} Banner", color=discord.Color.blurple())
        embed.set_image(url=guild.banner.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
