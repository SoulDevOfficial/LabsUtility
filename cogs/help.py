# This is the base of the help command and as of writing this, has yet to even be updated on the main bot. To add or remove commands, edit the json below.
import discord
from discord.ext import commands
from discord import app_commands

HELP_CATEGORIES = [
    {
        "name": "General",
        "commands": [
            {
                "name": "/help",
                "description": "Show the help menu."
            }
        ]
    },
    {
        "name": "Moderation",
        "commands": []
    }
]


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.index = 0

    def get_embed(self):
        category = HELP_CATEGORIES[self.index]

        embed = discord.Embed(
            title=f"**{category['name']}**",
            color=discord.Color.blurple()
        )

        if category["commands"]:
            for cmd in category["commands"]:
                embed.add_field(
                    name=cmd["name"],
                    value=cmd["description"],
                    inline=False
                )
        else:
            embed.add_field(
                name="No commands",
                value="Commands will be added soon.",
                inline=False
            )

        embed.set_footer(
            text=f"Category {self.index + 1}/{len(HELP_CATEGORIES)}"
        )
        return embed

    @discord.ui.button(label="â", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, _):
        self.index = (self.index - 1) % len(HELP_CATEGORIES)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="â¶", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, _):
        self.index = (self.index + 1) % len(HELP_CATEGORIES)
        await interaction.response.edit_message(embed=self.get_embed(), view=self)


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show the help menu")
    async def help(self, interaction: discord.Interaction):
        view = HelpView()
        await interaction.response.send_message(
            embed=view.get_embed(),
            view=view,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
