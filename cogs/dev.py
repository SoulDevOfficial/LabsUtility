import discord
from discord.ext import commands
from discord import app_commands
import hashlib
import base64
import json
import uuid
import re
import textwrap
from datetime import datetime
import urllib.parse
import binascii
import jwt
import difflib


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hash", description="Generate a hash")
    async def hash(
        self,
        interaction: discord.Interaction,
        algorithm: str,
        text: str
    ):
        try:
            h = hashlib.new(algorithm)
            h.update(text.encode())
            await interaction.response.send_message(
                f"**{algorithm.upper()}**\n```{h.hexdigest()}```",
                ephemeral=True
            )
        except Exception:
            await interaction.response.send_message("Invalid hash algorithm.", ephemeral=True)

    @hash.autocomplete("algorithm")
    async def hash_algos(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=a.upper(), value=a)
            for a in sorted(hashlib.algorithms_available)
            if current.lower() in a.lower()
        ][:25]

    @app_commands.command(name="base64-encode", description="Base64 encode text")
    async def b64_encode(self, interaction, text: str):
        await interaction.response.send_message(
            f"```{base64.b64encode(text.encode()).decode()}```",
            ephemeral=True
        )

    @app_commands.command(name="base64-decode", description="Base64 decode text")
    async def b64_decode(self, interaction, text: str):
        try:
            decoded = base64.b64decode(text).decode()
            await interaction.response.send_message(f"```{decoded}```", ephemeral=True)
        except Exception:
            await interaction.response.send_message("Invalid Base64.", ephemeral=True)

    @app_commands.command(name="json-validate", description="Validate JSON")
    async def json_validate(self, interaction, data: str):
        try:
            json.loads(data)
            await interaction.response.send_message("Valid JSON.", ephemeral=True)
        except json.JSONDecodeError as e:
            await interaction.response.send_message(f"Invalid JSON:\n```{e}```", ephemeral=True)

    @app_commands.command(name="json-format", description="Pretty-print JSON")
    async def json_format(self, interaction, data: str):
        try:
            formatted = json.dumps(json.loads(data), indent=2)
            await interaction.response.send_message(
                f"```json\n{formatted[:3900]}```",
                ephemeral=True
            )
        except Exception:
            await interaction.response.send_message("Invalid JSON.", ephemeral=True)

    @app_commands.command(name="regex-test", description="Test a regex pattern")
    async def regex_test(
        self,
        interaction: discord.Interaction,
        pattern: str,
        text: str
    ):
        try:
            matches = re.findall(pattern, text)
            result = matches if matches else "No matches."
            await interaction.response.send_message(
                f"```{result}```",
                ephemeral=True
            )
        except re.error as e:
            await interaction.response.send_message(f"Regex error:\n```{e}```", ephemeral=True)

    @app_commands.command(name="uuid", description="Generate a UUID")
    async def uuid_gen(self, interaction):
        await interaction.response.send_message(
            f"```{uuid.uuid4()}```",
            ephemeral=True
        )

    @app_commands.command(name="timestamp", description="Unix and Discord timestamps")
    async def timestamp(self, interaction):
        now = int(datetime.utcnow().timestamp())
        await interaction.response.send_message(
            f"Unix: `{now}`\nDiscord: `<t:{now}:F>`",
            ephemeral=True
        )

    @app_commands.command(name="wrap", description="Wrap text to width")
    async def wrap(
        self,
        interaction: discord.Interaction,
        width: int,
        text: str
    ):
        wrapped = "\n".join(textwrap.wrap(text, width))
        await interaction.response.send_message(
            f"```{wrapped[:3900]}```",
            ephemeral=True
        )

    @app_commands.command(name="length", description="Get string length")
    async def length(self, interaction, text: str):
        await interaction.response.send_message(
            f"Length: **{len(text)}**",
            ephemeral=True
        )

    @app_commands.command(name="url-encode", description="URL encode text")
    async def url_encode(self, interaction, text: str):
        encoded = urllib.parse.quote(text)
        await interaction.response.send_message(f"```{encoded}```", ephemeral=True)

    @app_commands.command(name="url-decode", description="URL decode text")
    async def url_decode(self, interaction, text: str):
        decoded = urllib.parse.unquote(text)
        await interaction.response.send_message(f"```{decoded}```", ephemeral=True)

    @app_commands.command(name="hex-encode", description="Encode text to hex")
    async def hex_encode(self, interaction, text: str):
        encoded = binascii.hexlify(text.encode()).decode()
        await interaction.response.send_message(f"```{encoded}```", ephemeral=True)

    @app_commands.command(name="hex-decode", description="Decode hex to text")
    async def hex_decode(self, interaction, text: str):
        try:
            decoded = binascii.unhexlify(text).decode()
            await interaction.response.send_message(f"```{decoded}```", ephemeral=True)
        except Exception:
            await interaction.response.send_message("Invalid hex.", ephemeral=True)

    @app_commands.command(name="jwt-decode", description="Decode a JWT (no verification)")
    async def jwt_decode(self, interaction, token: str):
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            await interaction.response.send_message(
                f"```json\n{json.dumps(decoded, indent=2)[:3900]}```",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"Invalid JWT:\n```{e}```", ephemeral=True)

    @app_commands.command(name="diff", description="Show diff between two strings")
    async def diff(self, interaction, a: str, b: str):
        d = difflib.unified_diff(
            a.splitlines(),
            b.splitlines(),
            lineterm="",
            fromfile="A",
            tofile="B"
        )
        output = "\n".join(d)[:3900]
        await interaction.response.send_message(
            f"```{output if output else 'No differences.'}```",
            ephemeral=True
        )

    @app_commands.command(name="password-strength", description="Estimate password strength")
    async def password_strength(self, interaction, password: str):
        length = len(password)
        unique_chars = len(set(password))
        strength = "Weak"
        if length >= 12 and unique_chars >= 8:
            strength = "Strong"
        elif length >= 8 and unique_chars >= 5:
            strength = "Medium"
        await interaction.response.send_message(
            f"Password length: {length}\nUnique characters: {unique_chars}\nEstimated strength: **{strength}**",
            ephemeral=True
        )

    async def cog_app_command_error(self, interaction, error):
        await interaction.response.send_message(
            "An error occurred.",
            ephemeral=True
        )
        raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(Dev(bot))
