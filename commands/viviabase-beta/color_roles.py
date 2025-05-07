"""
A Vivia extension that allows users to create roles with custom colors.

Vivia is licensed under the MIT License. For more information, see the LICENSE file.
TL;DR: you can use Vivia's code as long as you keep the original license intact.
Vivia is made open source in the hopes that you'll find her code useful.

If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

Have a great time using Vivia!
"""

import discord.ext as dext
from discord.ext import commands
from discord import Colour
from extras.viviatools import personality_message, block_in_dms

COLOR_ALIASES = {
    "black": "#000000",
    "white": "#FFFFFF",
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "orange": "#FFA500",
    "purple": "#800080",
    "pink": "#FFC0CB",
    "brown": "#A52A2A",
    "gray": "#808080",
    "teal": "#008080",
}

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")

async def setup(bot):
    await bot.add_cog(ColorRoles(bot))

class ColorRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="create_color_role",
        description="Assign yourself a role with a custom color.",
    )
    @block_in_dms
    async def create_color_role(self, ctx: commands.Context, color: str):
        """Create a role with a custom color."""

        guild = ctx.guild

        if not color.startswith("#") or len(color) != 7:
            # See if it's a hardcoded color
            color = color.lower()
            if color in COLOR_ALIASES:
                color = COLOR_ALIASES[color]
            else:
                await ctx.send(personality_message("color_roles.invalidcolor").replace("{color}", color))
                return

        # Make sure it's a valid hex color
        try:
            int(color[1:], 16)
        except ValueError:
            await ctx.send(personality_message("color_roles.invalidcolor").replace("{color}", color))
            return

        # See if we need to create the role
        if not any(role.name.startswith("Color Role - ") for role in guild.roles):
            # Convert hex color to rgb
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            role = await guild.create_role(
                name=f"Color Role - {color}",
                colour=Colour.from_rgb(r, g, b),
                reason=f"Created by {ctx.author.name}#{ctx.author.discriminator} with create_color_role command",
            )
        else:
            for role in guild.roles:
                if role.name == f"Color Role - {color}":
                    break

        await ctx.author.add_roles(
            role,
            reason=f"Created by {ctx.author.name}#{ctx.author.discriminator} with create_color_role command",
        )

        await ctx.send(
            personality_message("color_roles.createcolorrole")
            .replace("{role}", role.mention)
            .replace("{color}", color)
        )

        return

    @commands.hybrid_command(
        name="unassign-color-role",
        description="Remove your current custom color role.",
    )
    @block_in_dms
    async def unassign_color_role(self, ctx: commands.Context):
        """Remove your current custom color role."""

        for role in ctx.author.roles:
            if role.name.startswith("Color Role - "):
                await ctx.author.remove_roles(role)
                await ctx.send(personality_message("color_roles.removecolorrole"))
                return

        await ctx.send(personality_message("color_roles.nocolorrole"))

        return

    @dext.tasks.loop(hours=1)
    async def check_color_roles(self):
        """Automatically delete color roles that have no members."""
        while True:
            await self.bot.wait_until_ready()
            guilds = self.bot.guilds
            for guild in guilds:
                for role in guild.roles:
                    if role.name.startswith("Color Role - ") and role.members == []:
                        await role.delete(reason="Color role has no members.")
