import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime


BADGE_EMOJIS = {
    "staff": "👨‍💼",
    "partner": "🤝",
    "hypesquad": "🎉",
    "bug_hunter": "🐛",
    "bug_hunter_level_2": "🐞",
    "early_supporter": "💖",
    "verified_bot": "🤖",
    "verified_bot_developer": "🧑‍💻",
    "active_developer": "⚙️",
    "certified_moderator": "🛡️",
    "hypesquad_bravery": "🦁",
    "hypesquad_brilliance": "🧠",
    "hypesquad_balance": "⚖️",
}


def fmt(ts: datetime | None):
    return ts.strftime("%Y-%m-%d %H:%M:%S") if ts else "Unavailable"


def get_badges(user: discord.User):
    flags = user.public_flags
    badges = []

    for name in dir(flags):
        if name.startswith("_"):
            continue

        try:
            value = getattr(flags, name)
        except Exception:
            continue

        if value is True:
            emoji = BADGE_EMOJIS.get(name, "❔")
            pretty = name.replace("_", " ").title()
            badges.append(f"{emoji} {pretty}")

    return badges


async def resolve_member(guild: discord.Guild | None, user_id: int):
    if not guild:
        return None
    member = guild.get_member(user_id)
    if member:
        return member
    try:
        return await guild.fetch_member(user_id)
    except discord.NotFound:
        return None


class UserInfoView(discord.ui.View):
    def __init__(self, user: discord.User, member: discord.Member | None):
        super().__init__(timeout=120)
        self.user = user
        self.member = member

    async def reply(self, interaction: discord.Interaction, embed: discord.Embed):
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Badges", style=discord.ButtonStyle.secondary)
    async def badges(self, interaction: discord.Interaction, _):
        embed = discord.Embed(title="Badges", color=discord.Color.blurple())
        badges = get_badges(self.user)
        embed.description = "\n".join(badges) if badges else "None"
        await self.reply(interaction, embed)

    @discord.ui.button(label="Presence", style=discord.ButtonStyle.secondary)
    async def presence(self, interaction: discord.Interaction, _):
        embed = discord.Embed(title="Presence", color=discord.Color.blurple())
        if self.member:
            embed.add_field(name="Status", value=str(self.member.status))
            embed.add_field(
                name="Activities",
                value=", ".join(a.name for a in self.member.activities) or "None",
                inline=False
            )
        else:
            embed.description = "Unavailable"
        await self.reply(interaction, embed)

    @discord.ui.button(label="Guild Info", style=discord.ButtonStyle.secondary)
    async def guild_info(self, interaction: discord.Interaction, _):
        embed = discord.Embed(title="Guild Info", color=discord.Color.blurple())
        if self.member:
            embed.add_field(name="Nickname", value=self.member.nick or "None")
            embed.add_field(name="Joined At", value=fmt(self.member.joined_at))
            embed.add_field(name="Boosting", value="Yes" if self.member.premium_since else "No")
            embed.add_field(
                name="Roles",
                value=", ".join(r.mention for r in self.member.roles[1:]) or "None",
                inline=False
            )
        else:
            embed.description = "Unavailable"
        await self.reply(interaction, embed)

    @discord.ui.button(label="Voice", style=discord.ButtonStyle.secondary)
    async def voice(self, interaction: discord.Interaction, _):
        embed = discord.Embed(title="Voice State", color=discord.Color.blurple())
        if self.member and self.member.voice:
            v = self.member.voice
            embed.add_field(name="Channel", value=v.channel.name)
            embed.add_field(name="Muted", value=v.mute)
            embed.add_field(name="Deafened", value=v.deaf)
            embed.add_field(name="Streaming", value=v.self_stream)
        else:
            embed.description = "Unavailable"
        await self.reply(interaction, embed)

    @discord.ui.button(label="Permissions", style=discord.ButtonStyle.secondary)
    async def permissions(self, interaction: discord.Interaction, _):
        embed = discord.Embed(title="Permissions", color=discord.Color.blurple())
        if self.member:
            perms = [p.replace("_", " ").title() for p, v in self.member.guild_permissions if v]
            embed.description = ", ".join(perms) if perms else "None"
        else:
            embed.description = "Unavailable"
        await self.reply(interaction, embed)


class Userinfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Show detailed user information")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User | None = None):
        user = user or interaction.user
        member = await resolve_member(interaction.guild, user.id)

        embed = discord.Embed(title=str(user), color=discord.Color.blurple())
        embed.set_thumbnail(url=user.display_avatar.url)

        if user.banner:
            embed.set_image(url=user.banner.url)

        embed.add_field(name="User ID", value=user.id)
        embed.add_field(name="Bot", value=user.bot)
        embed.add_field(name="Created At", value=fmt(user.created_at))
        embed.add_field(
            name="Guild Status",
            value="In Server" if member else "Not in Server",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            view=UserInfoView(user, member),
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Userinfo(bot))
