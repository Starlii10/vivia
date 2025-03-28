#!/usr/bin/env python
"""
This is the help command, part of the ViviaBase extension package.

Vivia is licensed under the MIT License. For more information, see the LICENSE file.
TL:DR: you can use Vivia's code as long as you keep the original license intact.
Vivia is made open source in the hopes that you'll find her code useful.

If you'd like to contribute, please check out the GitHub repository at https://github.com/starlii10/vivia.

Have a great time using Vivia!
"""

from discord import app_commands
from discord.ext import commands
from extras.viviatools import help_msg, personality_message

if __name__ == "__main__":
    raise Exception("Vivia extensions should not be run as a script.")


async def setup(bot: commands.Bot):  # for extension loading
    """
    The main setup function for an extension.
    """
    bot.add_command(help)


@commands.hybrid_command()
@app_commands.describe(extension="The name of the extension you want help with. ")
async def help(ctx: commands.Context, extension: str = "core"):
    """
    Help command.
    """
    await ctx.author.send(help_msg(extension))
    await ctx.send(
        personality_message("base.helpsent").replace("{user}", str(ctx.author)),
        ephemeral=True,
    )
